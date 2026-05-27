"""
cadastros/os_pdf.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ordem de Serviço — PDF profissional (A4 landscape)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import io
import os as _os
from datetime import datetime

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, PageBreak, HRFlowable,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─── Cores ───────────────────────────────────────────────────────────────────
_AZUL_ESCURO = "#0D1B2A"
_AZUL_MEDIO  = "#1B3A5C"
_AZUL_HEADER = "#1F4E79"
_AZUL_DEST   = "#4D8DF0"
_BRANCO      = "#FFFFFF"
_CINZA_BG    = "#F2F5F9"
_CINZA_TXT   = "#555555"
_CINZA_LIGHT = "#E8ECF0"
_VERDE       = "#2D7A4F"
_VERMELHO    = "#C0392B"
_LARANJA     = "#E67E22"


def _s(txt, size=8, bold=False, color=_CINZA_TXT, align=TA_LEFT):
    """Atalho para Paragraph style."""
    return ParagraphStyle(
        'tmp', parent=getSampleStyleSheet()['Normal'],
        fontSize=size, leading=size + 2,
        fontName='Helvetica-Bold' if bold else 'Helvetica',
        textColor=HexColor(color), alignment=align,
    )


def _p(txt, style=None):
    """Atalho para Paragraph."""
    if style is None:
        style = _s(8)
    if txt is None:
        txt = ''
    return Paragraph(str(txt).replace('\n', '<br/>'), style)


def _safe_file_path(field):
    """Retorna o path absoluto de um ImageField, ou None."""
    try:
        if field and hasattr(field, 'path') and _os.path.exists(field.path):
            return field.path
    except Exception:
        pass
    return None


def _img_field(field, max_w=50*mm, max_h=35*mm):
    """Cria um flowable Image de um ImageField, ou None."""
    path = _safe_file_path(field)
    if not path:
        return None
    try:
        img = Image(path)
        if img.drawWidth <= 0 or img.drawHeight <= 0:
            return None
        ratio = min(max_w / img.drawWidth, max_h / img.drawHeight, 1.0)
        img.drawWidth *= ratio
        img.drawHeight *= ratio
        return img
    except Exception:
        return None


def _header_block(os_obj):
    """Cabeçalho principal com logo, empresa e dados da OS."""
    elements = []

    # Tabela de cabeçalho
    title_style = _s(14, bold=True, color=_BRANCO, align=TA_LEFT)
    sub_style = _s(9, color='#A0B4CC', align=TA_LEFT)
    os_style = _s(22, bold=True, color=_AZUL_DEST, align=TA_RIGHT)
    status_style = _s(9, color='#A0B4CC', align=TA_RIGHT)

    status_map = dict(os_obj.STATUS_CHOICES)
    status_txt = status_map.get(os_obj.status, os_obj.status)

    header_data = [
        [
            Paragraph('JR SEGURANÇA', title_style),
            Paragraph(f'OS-{os_obj.numero}', os_style),
        ],
        [
            Paragraph('Ordem de Serviço — Impressão', sub_style),
            Paragraph(f'Status: {status_txt}', status_style),
        ],
    ]

    header_table = Table(header_data, colWidths=[200*mm, 90*mm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(_AZUL_ESCURO)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, -1), 15),
        ('RIGHTPADDING', (-1, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
        ('SPAN', (0, 0), (0, 1)),  # não precisa span, mantém separado
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 6*mm))
    return elements


def _section_header(title):
    """Cabeçalho de seção azul escuro."""
    style = ParagraphStyle('sh', parent=getSampleStyleSheet()['Normal'],
                           fontSize=10, fontName='Helvetica-Bold',
                           textColor=HexColor(_BRANCO))
    data = [[Paragraph(title, style)]]
    t = Table(data, colWidths=[290*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(_AZUL_MEDIO)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


def _info_row(label, value, label2=None, value2=None):
    """Linha com 2 campos lado a lado."""
    ls = _s(7, bold=True, color=_CINZA_TXT)
    vs = _s(9, color='#1A1A1A')
    lls = _s(7, bold=True, color=_CINZA_TXT)
    vvs = _s(9, color='#1A1A1A')

    row = [
        [Paragraph(label, ls), Paragraph(str(value or '—'), vs)],
    ]
    if label2 is not None:
        row[0].extend([Paragraph(label2, lls), Paragraph(str(value2 or '—'), vvs)])
        widths = [40*mm, 105*mm, 40*mm, 105*mm]
    else:
        widths = [40*mm, 250*mm]

    t = Table(row, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), HexColor(_CINZA_LIGHT)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#CCCCCC')),
    ]))
    if label2 is not None:
        t.setStyle(TableStyle([
            ('BACKGROUND', (2, 0), (2, 0), HexColor(_CINZA_LIGHT)),
        ]))
    return t


def _info_table(fields):
    """Monta tabela de informações a partir de lista de (label, value, label, value)."""
    elements = []
    for row in fields:
        if len(row) == 4:
            elements.append(_info_row(row[0], row[1], row[2], row[3]))
        elif len(row) == 2:
            elements.append(_info_row(row[0], row[1]))
    return elements


def _marco_table(op):
    """Tabela de marcos operacionais (horários + KM + GPS)."""
    if not op:
        return []

    MARCOS = [
        ('Início de Viagem',    op.inicio_viagem,    op.km_inicio_viagem,
         op.gps_inicio_viagem_lat, op.gps_inicio_viagem_lng),
        ('Chegada Operação',    op.chegada_operacao, op.km_chegada_operacao,
         op.gps_chegada_operacao_lat, op.gps_chegada_operacao_lng),
        ('Início Operação',     op.inicio_operacao,  op.km_inicio_operacao,
         op.gps_inicio_operacao_lat, op.gps_inicio_operacao_lng),
        ('Término Operação',    op.termino_operacao, op.km_termino_operacao,
         op.gps_termino_operacao_lat, op.gps_termino_operacao_lng),
        ('Término de Viagem',   op.termino_viagem,   op.km_termino_viagem,
         op.gps_termino_viagem_lat, op.gps_termino_viagem_lng),
    ]

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(8, color='#1A1A1A')

    header = ['Marco', 'Data/Hora', 'KM', 'Duração', 'Latitude', 'Longitude']
    data = [[Paragraph(h, hdr) for h in header]]

    prev_dt = None
    for nome, dt, km, lat, lng in MARCOS:
        dt_str = dt.strftime('%d/%m/%Y %H:%M') if dt else '—'
        km_str = str(km) if km else '—'
        dur = ''
        if dt and prev_dt:
            delta = abs((dt - prev_dt).total_seconds())
            dur = f'{int(delta // 3600):02d}:{int((delta % 3600) // 60):02d}'
        lat_str = f'{lat:.5f}' if lat else '—'
        lng_str = f'{lng:.5f}' if lng else '—'
        data.append([Paragraph(nome, cel), Paragraph(dt_str, cel),
                     Paragraph(km_str, cel), Paragraph(dur, cel),
                     Paragraph(lat_str, cel), Paragraph(lng_str, cel)])
        prev_dt = dt

    t = Table(data, colWidths=[40*mm, 42*mm, 20*mm, 22*mm, 30*mm, 30*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(_AZUL_HEADER)),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(_BRANCO)),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor(_BRANCO), HexColor(_CINZA_BG)]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return [t]


def _veiculos_table(veiculos):
    """Tabela de veículos escoltados."""
    if not veiculos:
        return []

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(8, color='#1A1A1A')

    header = ['Nº', 'Veículo', 'Placa Cavalo', 'Placa Carreta', 'Placa Carreta 2', 'Motorista']
    data = [[Paragraph(h, hdr) for h in header]]

    for i, v in enumerate(veiculos, 1):
        data.append([
            Paragraph(str(i), cel),
            Paragraph(v.veiculo or '—', cel),
            Paragraph(v.placa_cavalo or '—', cel),
            Paragraph(v.placa_carreta or '—', cel),
            Paragraph(v.placa_carreta2 or '—', cel),
            Paragraph(v.motorista or '—', cel),
        ])

    t = Table(data, colWidths=[12*mm, 55*mm, 40*mm, 40*mm, 40*mm, 55*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(_AZUL_HEADER)),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(_BRANCO)),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor(_BRANCO), HexColor(_CINZA_BG)]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return [t]


def _paradas_table(paradas):
    """Tabela de paradas registradas."""
    if not paradas:
        return []

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(8, color='#1A1A1A')

    header = ['Motivo', 'Descrição', 'Início', 'Fim', 'Duração']
    data = [[Paragraph(h, hdr) for h in header]]

    for p in paradas:
        dur = ''
        if p.duracao_minutos is not None:
            dur = f'{p.duracao_minutos} min'
        data.append([
            Paragraph(p.get_motivo_display(), cel),
            Paragraph(p.descricao or '—', cel),
            Paragraph(p.inicio.strftime('%d/%m %H:%M') if p.inicio else '—', cel),
            Paragraph(p.fim.strftime('%d/%m %H:%M') if p.fim else '—', cel),
            Paragraph(dur or '—', cel),
        ])

    t = Table(data, colWidths=[35*mm, 110*mm, 35*mm, 35*mm, 25*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(_AZUL_HEADER)),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(_BRANCO)),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor(_BRANCO), HexColor(_CINZA_BG)]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return [t]


def _incidentes_table(incidentes):
    """Tabela de incidentes."""
    if not incidentes:
        return []

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(8, color='#1A1A1A')

    header = ['Tipo', 'Gravidade', 'Descrição', 'Data/Hora', 'Nº BO']
    data = [[Paragraph(h, hdr) for h in header]]

    for inc in incidentes:
        grav_colors = {'baixa': _VERDE, 'media': _LARANJA, 'alta': _VERMELHO, 'critica': _VERMELHO}
        gc = grav_colors.get(inc.gravidade, _CINZA_TXT)
        data.append([
            Paragraph(inc.get_tipo_display(), cel),
            Paragraph(f'<font color="#{gc}">{inc.get_gravidade_display()}</font>', cel),
            Paragraph(inc.descricao[:100] or '—', cel),
            Paragraph(inc.ocorrido_em.strftime('%d/%m/%Y %H:%M') if inc.ocorrido_em else '—', cel),
            Paragraph(inc.bo_numero or '—', cel),
        ])

    t = Table(data, colWidths=[40*mm, 25*mm, 120*mm, 40*mm, 35*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(_AZUL_HEADER)),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(_BRANCO)),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor(_BRANCO), HexColor(_CINZA_BG)]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return [t]


def _despesas_table(despesas):
    """Tabela de despesas."""
    if not despesas:
        return []

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(8, color='#1A1A1A')

    header = ['Tipo', 'Natureza', 'Descrição', 'Valor (R$)', 'Data/Hora']
    data = [[Paragraph(h, hdr) for h in header]]

    total = 0
    for d in despesas:
        val = float(d.valor)
        if d.natureza == 'despesa':
            total += val
        else:
            total -= val
        data.append([
            Paragraph(d.get_tipo_display(), cel),
            Paragraph(d.get_natureza_display(), cel),
            Paragraph(d.descricao or '—', cel),
            Paragraph(f'{val:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'), cel),
            Paragraph(d.ocorrido_em.strftime('%d/%m/%Y %H:%M') if d.ocorrido_em else '—', cel),
        ])

    # Linha de total
    tot_style = _s(8, bold=True, color=_VERMELHO)
    total_str = f'{total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    data.append([
        Paragraph('', tot_style), Paragraph('', tot_style),
        Paragraph('TOTAL', tot_style),
        Paragraph(f'R$ {total_str}', tot_style),
        Paragraph('', tot_style),
    ])

    t = Table(data, colWidths=[35*mm, 25*mm, 115*mm, 30*mm, 40*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(_AZUL_HEADER)),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(_BRANCO)),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [HexColor(_BRANCO), HexColor(_CINZA_BG)]),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor(_CINZA_LIGHT)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return [t]


def _fotos_grid(fotos_dict, marcos_lista, titulo='Fotos dos Marcos'):
    """Grid de fotos dos marcos (2 por linha)."""
    elements = []

    has_photos = any(fotos_dict.get(m[0]) for m in marcos_lista)
    if not has_photos:
        return elements

    elements.append(Spacer(1, 4*mm))
    elements.append(_section_header(titulo))
    elements.append(Spacer(1, 2*mm))

    style_cap = _s(7, bold=True, color=_AZUL_MEDIO)

    rows = []
    row = []
    count = 0
    for key, label in marcos_lista:
        url = fotos_dict.get(key)
        if url:
            path = _os.path.join(settings.MEDIA_ROOT, url.replace('/media/', ''))
            if _os.path.exists(path):
                try:
                    img = Image(path)
                    if img.drawWidth <= 0 or img.drawHeight <= 0:
                        continue
                    ratio = min(55*mm / img.drawWidth, 35*mm / img.drawHeight, 1.0)
                    img.drawWidth *= ratio
                    img.drawHeight *= ratio
                    cell = [img, Paragraph(label, style_cap)]
                    row.append(cell)
                    count += 1
                    if count % 2 == 0:
                        rows.append(row)
                        row = []
                except Exception:
                    pass

    if row:
        # Pad with empty cell
        row.append(['', ''])
        rows.append(row)

    if rows:
        # Flatten: each cell has image + caption
        table_data = []
        for r in rows:
            img_row = []
            for cell in r:
                if isinstance(cell, list) and len(cell) == 2:
                    from reportlab.platypus import KeepTogether
                    img_row.append(KeepTogether([cell[0], cell[1]]))
                else:
                    img_row.append('')
            table_data.append(img_row)

        t = Table(table_data, colWidths=[145*mm, 145*mm])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
            ('INNERGRID', (0, 0), (-1, -1), 0.3, HexColor('#DDDDDD')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(t)

    return elements


def _assinaturas_block(assinaturas):
    """Bloco de assinaturas digitais."""
    if not assinaturas:
        return []

    elements = []
    elements.append(Spacer(1, 4*mm))
    elements.append(_section_header('Assinaturas Digitais'))
    elements.append(Spacer(1, 2*mm))

    style_nom = _s(8, bold=True, color=_AZUL_MEDIO)
    style_tip = _s(7, color=_CINZA_TXT)

    cells = []
    for a in assinaturas:
        img = _img_field(a.imagem, max_w=60*mm, max_h=25*mm)
        cell_content = []
        if img:
            cell_content.append(img)
        cell_content.append(Paragraph(a.nome, style_nom))
        cell_content.append(Paragraph(a.get_tipo_display(), style_tip))
        cells.append(cell_content)

    # 2 assinaturas por linha
    rows = []
    for i in range(0, len(cells), 2):
        row = cells[i:i+2]
        while len(row) < 2:
            row.append('')
        rows.append(row)

    table_data = []
    for r in rows:
        from reportlab.platypus import KeepTogether
        table_data.append([
            KeepTogether(r[0]) if isinstance(r[0], list) else r[0],
            KeepTogether(r[1]) if isinstance(r[1], list) else r[1],
        ])

    if table_data:
        t = Table(table_data, colWidths=[145*mm, 145*mm])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
            ('INNERGRID', (0, 0), (-1, -1), 0.3, HexColor('#DDDDDD')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(t)

    return elements


def gerar_os_pdf(request, pk):
    """Gera PDF profissional da OS e retorna HttpResponse."""
    from .models import (
        OrdemServico, OSOperacional, FotoMarco, AssinaturaOS,
        VeiculoEscoltado, FotoVeiculoEscoltado,
        Parada, FotoParada, Incidente, DespesaOS, Rastreador,
    )

    os_obj = OrdemServico.objects.select_related(
        'cliente', 'equipe', 'equipe__viatura'
    ).get(pk=pk)

    op = getattr(os_obj, 'operacional', None)
    veiculos = list(os_obj.veiculos.order_by('ordem'))
    paradas = list(os_obj.paradas.all())
    incidentes = list(os_obj.incidentes.all())
    despesas = []  # DespesaOS sem FK para OS no banco
    assinaturas = list(os_obj.assinaturas.all())

    # Fotos dos marcos
    fotos_marco = {}
    for foto in FotoMarco.objects.filter(os=os_obj):
        fotos_marco[foto.marco] = foto.foto.url

    MARCOS_LISTA = [
        ('inicio_viagem',     'Início de Viagem'),
        ('chegada_operacao',  'Chegada Operação'),
        ('inicio_operacao',   'Início Operação'),
        ('termino_operacao',  'Término Operação'),
        ('termino_viagem',    'Término de Viagem'),
    ]

    # ── Montar PDF ───────────────────────────────────────────────────────────
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=10*mm, rightMargin=10*mm,
        topMargin=10*mm, bottomMargin=10*mm,
        title=f'OS-{os_obj.numero}',
        author='JR Segurança',
    )

    elements = []

    # ── Cabeçalho ──
    elements.extend(_header_block(os_obj))

    # ── Dados da OS ──
    elements.append(_section_header('Dados da Ordem de Serviço'))
    elements.append(Spacer(1, 2*mm))

    elements.extend(_info_table([
        ('Cliente', os_obj.cliente.razao_social if os_obj.cliente else '—',
         'Nº OS', f'OS-{os_obj.numero}'),
        ('Solicitante', os_obj.solicitante or '—',
         'Forma Solic.', os_obj.get_forma_solicitacao_display()),
        ('Tipo Viagem', os_obj.get_tipo_viagem_display(),
         'Imediata', 'Sim' if os_obj.imediata else 'Não'),
        ('Cidade Origem', f'{os_obj.cidade_origem}/{os_obj.uf_origem}',
         'Cidade Destino', f'{os_obj.cidade_destino}/{os_obj.uf_destino}'),
        ('Previsão Início', os_obj.previsao_inicio.strftime('%d/%m/%Y %H:%M') if os_obj.previsao_inicio else '—',
         'Previsão Retorno', os_obj.previsao_retorno.strftime('%d/%m/%Y %H:%M') if os_obj.previsao_retorno else '—'),
    ]))

    # ── Equipe ──
    elements.append(Spacer(1, 4*mm))
    elements.append(_section_header('Equipe'))
    elements.append(Spacer(1, 2*mm))

    eq_nome = os_obj.snap_equipe_nome or (os_obj.equipe.nome if os_obj.equipe else '—')
    ag1 = os_obj.snap_agente1_nome or '—'
    ag2 = os_obj.snap_agente2_nome or '—'
    vtr = f'{os_obj.snap_viatura_modelo or "—"} / {os_obj.snap_viatura_placa or "—"}'

    elements.extend(_info_table([
        ('Equipe', eq_nome,
         'Viatura', vtr),
        ('Agente 1', ag1,
         'Agente 2', ag2),
    ]))

    # Dados detalhados dos agentes (CPF, RG, CNH, CNV)
    if os_obj.snap_agente1_cpf or os_obj.snap_agente2_cpf:
        elements.append(Spacer(1, 1*mm))
        elements.extend(_info_table([
            ('CPF Ag.1', os_obj.snap_agente1_cpf or '—',
             'CPF Ag.2', os_obj.snap_agente2_cpf or '—'),
            ('RG Ag.1', os_obj.snap_agente1_rg or '—',
             'RG Ag.2', os_obj.snap_agente2_rg or '—'),
            ('CNH Ag.1', os_obj.snap_agente1_cnh or '—',
             'CNH Ag.2', os_obj.snap_agente2_cnh or '—'),
            ('CNV Ag.1', os_obj.snap_agente1_cnv or '—',
             'CNV Ag.2', os_obj.snap_agente2_cnv or '—'),
        ]))

    # ── Marcos Operacionais ──
    if op:
        elements.append(Spacer(1, 4*mm))
        elements.append(_section_header('Marcos Operacionais'))
        elements.append(Spacer(1, 2*mm))
        elements.extend(_marco_table(op))

        # Pedágio
        if op.pedagio and op.pedagio > 0:
            elements.append(Spacer(1, 1*mm))
            ped_str = f'{float(op.pedagio):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
            elements.extend(_info_table([
                ('Pedágio', f'R$ {ped_str}',
                 'Nº Folha', op.numero_folha or '—'),
            ]))

    # ── Veículos Escoltados ──
    if veiculos:
        elements.append(Spacer(1, 4*mm))
        elements.append(_section_header('Veículos Escoltados'))
        elements.append(Spacer(1, 2*mm))
        elements.extend(_veiculos_table(veiculos))

    # ── Paradas ──
    if paradas:
        elements.append(Spacer(1, 4*mm))
        elements.append(_section_header('Paradas Registradas'))
        elements.append(Spacer(1, 2*mm))
        elements.extend(_paradas_table(paradas))

    # ── Incidentes ──
    if incidentes:
        elements.append(Spacer(1, 4*mm))
        elements.append(_section_header('Incidentes'))
        elements.append(Spacer(1, 2*mm))
        elements.extend(_incidentes_table(incidentes))

    # ── Despesas ──
    if despesas:
        elements.append(Spacer(1, 4*mm))
        elements.append(_section_header('Despesas'))
        elements.append(Spacer(1, 2*mm))
        elements.extend(_despesas_table(despesas))

    # ── Fotos dos Marcos ──
    elements.extend(_fotos_grid(fotos_marco, MARCOS_LISTA))

    # ── Assinaturas ──
    elements.extend(_assinaturas_block(assinaturas))

    # ── Observações ──
    if os_obj.observacoes:
        elements.append(Spacer(1, 4*mm))
        elements.append(_section_header('Observações'))
        elements.append(Spacer(1, 2*mm))
        obs_style = _s(9, color='#1A1A1A')
        elements.append(Paragraph(os_obj.observacoes.replace('\n', '<br/>'), obs_style))

    # ── Rodapé ──
    elements.append(Spacer(1, 6*mm))
    now_str = datetime.now().strftime('%d/%m/%Y %H:%M')
    footer_style = _s(7, color=_CINZA_TXT, align=TA_CENTER)
    elements.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#CCCCCC')))
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph(
        f'JR Segurança e Vigilância Patrimonial Ltda — Depto. de Escolta Armada | '
        f'Gerado em {now_str}',
        footer_style
    ))

    # ── Build ──
    doc.build(elements)
    buffer.seek(0)

    from django.http import FileResponse
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="OS-{os_obj.numero}.pdf"'
    return response
