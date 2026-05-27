"""
cadastros/os_pdf.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ordem de Serviço — PDF compacto (A4 portrait, 2 páginas)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import io
import logging
import os as _os
from datetime import datetime

from django.conf import settings

logger = logging.getLogger(__name__)

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, KeepTogether, PageBreak,
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

# Largura útil A4 portrait com margens 10mm
_W = A4[0] - 20*mm  # ~190mm


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _s(size=8, bold=False, color=_CINZA_TXT, align=TA_LEFT):
    """Atalho para ParagraphStyle."""
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
        if img.drawWidth > 300*mm or img.drawHeight > 300*mm:
            return None
        return img
    except Exception:
        logger.exception("Erro ao carregar imagem %s", path)
        return None


def _field(label, value, label_w=28*mm, value_w=55*mm):
    """Par label + valor inline."""
    ls = _s(6, bold=True, color=_CINZA_TXT)
    vs = _s(7, color='#1A1A1A')
    return [
        Paragraph(label, ls),
        Paragraph(str(value or '—'), vs),
    ]


# ─── Página 1 ────────────────────────────────────────────────────────────────

def _header_block(os_obj):
    """Header escuro: JR SEGURANÇA + OS + Status."""
    title_style = _s(12, bold=True, color=_BRANCO)
    os_style = _s(14, bold=True, color=_AZUL_DEST, align=TA_RIGHT)

    status_map = dict(os_obj.STATUS_CHOICES)
    status_txt = status_map.get(os_obj.status, os_obj.status)

    # Badge de status
    status_colors = {
        'aberta': _AZUL_DEST, 'em_viagem': _LARANJA, 'em_operacao': _VERDE,
        'encerrando': _LARANJA, 'concluida': _VERDE, 'finalizada': _VERDE,
        'cancelada': _VERMELHO,
    }
    sc = status_colors.get(os_obj.status, _CINZA_TXT)
    status_style = _s(8, bold=True, color=sc)

    header_data = [[
        Paragraph('JR SEGURANÇA', title_style),
        Paragraph(f'OS-{os_obj.numero}', os_style),
    ]]
    t = Table(header_data, colWidths=[_W * 0.6, _W * 0.4])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(_AZUL_ESCURO)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    # Linha de status
    st = Table(
        [[Paragraph(f'Status: {status_txt}', status_style)]],
        colWidths=[_W],
    )
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(_CINZA_LIGHT)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))

    return [t, Spacer(1, 1*mm), st, Spacer(1, 3*mm)]


def _section_header(title):
    """Barra de seção azul."""
    style = _s(8, bold=True, color=_BRANCO)
    data = [[Paragraph(title, style)]]
    t = Table(data, colWidths=[_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(_AZUL_MEDIO)),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def _info_grid(rows, col_widths=None):
    """Grid de campos (label: valor) em tabela compacta."""
    if col_widths is None:
        col_widths = [_W]
    ls = _s(6, bold=True, color=_CINZA_TXT)
    vs = _s(7, color='#1A1A1A')

    data = []
    for row in rows:
        cells = []
        for label, value in row:
            cells.append(Paragraph(f'{label}: ', ls))
            cells.append(Paragraph(str(value or '—'), vs))
        data.append(cells)

    # Calcular larguras: cada par (label, valor) ocupa espaço
    n_pairs = len(rows[0]) if rows else 1
    pair_w = _W / n_pairs
    widths = []
    for _ in range(n_pairs):
        widths.extend([22*mm, pair_w - 22*mm])

    t = Table(data, colWidths=widths)
    style_cmds = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#CCCCCC')),
    ]
    # Fundo cinza nos labels
    for i in range(n_pairs):
        label_col = i * 2
        style_cmds.append(('BACKGROUND', (label_col, 0), (label_col, -1), HexColor(_CINZA_LIGHT)))
    t.setStyle(TableStyle(style_cmds))
    return t


def _identificacao_os_block(os_obj):
    """Seção IDENTIFICAÇÃO DA OS."""
    elements = []
    elements.append(_section_header('IDENTIFICAÇÃO DA OS'))
    elements.append(Spacer(1, 1*mm))

    elements.append(_info_grid([
        [('Nº OS / FOLHA', f'OS-{os_obj.numero}'),
         ('TIPO OPERAÇÃO', os_obj.get_tipo_viagem_display()),
         ('STATUS', dict(os_obj.STATUS_CHOICES).get(os_obj.status, os_obj.status))],
    ]))
    elements.append(Spacer(1, 0.5*mm))

    elements.append(_info_grid([
        [('EMPRESA CONTRATANTE', os_obj.cliente.razao_social if os_obj.cliente else '—'),
         ('SOLICITANTE', os_obj.solicitante or '—')],
    ]))
    elements.append(Spacer(1, 0.5*mm))

    data_inicio = os_obj.previsao_inicio.strftime('%d/%m/%Y') if os_obj.previsao_inicio else '—'
    hora_inicio = os_obj.previsao_inicio.strftime('%H:%M') if os_obj.previsao_inicio else '—'

    elements.append(_info_grid([
        [('DATA INÍCIO', data_inicio),
         ('HORA INÍCIO', hora_inicio),
         ('TEL / CONTATO', '—')],
    ]))
    elements.append(Spacer(1, 0.5*mm))

    elements.append(_info_grid([
        [('FORMA SOLICITAÇÃO', os_obj.get_forma_solicitacao_display())],
    ]))
    elements.append(Spacer(1, 2*mm))
    return elements


def _trajeto_block(os_obj):
    """Seção TRAJETO / ROTA."""
    elements = []
    elements.append(_section_header('TRAJETO / ROTA'))
    elements.append(Spacer(1, 1*mm))

    elements.append(_info_grid([
        [('CIDADE ORIGEM', os_obj.cidade_origem or '—'),
         ('UF', os_obj.uf_origem or '—'),
         ('CIDADE DESTINO', os_obj.cidade_destino or '—'),
         ('UF', os_obj.uf_destino or '—')],
    ]))
    elements.append(Spacer(1, 2*mm))
    return elements


def _agente_block(numero, nome, cpf, rg, contato, cnh, val_cnh, cnv, val_cnv, endereco, status='Ativo'):
    """Bloco de identificação de agente individual."""
    elements = []

    # Header do agente com badge de status
    hdr_style = _s(8, bold=True, color=_BRANCO)
    status_style = _s(7, bold=True, color=_VERDE if status == 'Ativo' else _VERMELHO)

    hdr_data = [[
        Paragraph(f'IDENTIFICAÇÃO DO AGENTE {numero}', hdr_style),
        Paragraph(status or '—', status_style),
    ]]
    hdr = Table(hdr_data, colWidths=[_W * 0.8, _W * 0.2])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), HexColor(_AZUL_MEDIO)),
        ('BACKGROUND', (1, 0), (1, 0), HexColor(_CINZA_LIGHT)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(hdr)
    elements.append(Spacer(1, 0.5*mm))

    # Dados do agente
    elements.append(_info_grid([
        [('NOME COMPLETO', nome),
         ('CPF', cpf or '—'),
         ('RG', rg or '—'),
         ('CONTATO', contato or '—')],
    ]))
    elements.append(Spacer(1, 0.3*mm))

    elements.append(_info_grid([
        [('CNH', cnh or '—'),
         ('VAL. CNH', val_cnh or '—'),
         ('CNV', cnv or '—'),
         ('VAL. CNV', val_cnv or '—')],
    ]))
    elements.append(Spacer(1, 0.3*mm))

    elements.append(_info_grid([
        [('ENDEREÇO', endereco or '—')],
    ]))
    elements.append(Spacer(1, 2*mm))
    return elements


def _viatura_block(os_obj):
    """Seção VIATURA."""
    elements = []
    elements.append(_section_header('VIATURA'))
    elements.append(Spacer(1, 1*mm))

    modelo = os_obj.snap_viatura_modelo or '—'
    cor = os_obj.snap_viatura_cor or '—'
    frota = os_obj.snap_viatura_frota or '—'
    placa = os_obj.snap_viatura_placa or '—'
    mct = os_obj.snap_viatura_mct or '—'

    # Buscar RENAVAN da viatura via equipe
    renavan = '—'
    if os_obj.equipe and os_obj.equipe.viatura:
        renavan = os_obj.equipe.viatura.renavam or '—'

    elements.append(_info_grid([
        [('MODELO', modelo),
         ('COR', cor),
         ('FROTA', frota),
         ('PLACA', placa)],
    ]))
    elements.append(Spacer(1, 0.3*mm))

    elements.append(_info_grid([
        [('RENAVAN', renavan),
         ('MCT / ID', mct)],
    ]))
    elements.append(Spacer(1, 2*mm))
    return elements


def _dados_operacao_block(op):
    """Seção DADOS DA OPERAÇÃO — tabela de marcos."""
    if not op:
        return []

    elements = []
    elements.append(_section_header('DADOS DA OPERAÇÃO'))
    elements.append(Spacer(1, 1*mm))

    MARCOS = [
        ('Previsão de Início', op.os.previsao_inicio, None),
        ('Início de Viagem', op.inicio_viagem, op.km_inicio_viagem),
        ('Chegada Operação', op.chegada_operacao, op.km_chegada_operacao),
        ('Início Operação', op.inicio_operacao, op.km_inicio_operacao),
        ('Término Operação', op.termino_operacao, op.km_termino_operacao),
        ('Término de Viagem', op.termino_viagem, op.km_termino_viagem),
    ]

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(7, color='#1A1A1A')

    data = [[
        Paragraph('MARCO', hdr),
        Paragraph('DATA / HORA', hdr),
        Paragraph('KM', hdr),
    ]]

    for nome, dt, km in MARCOS:
        dt_str = dt.strftime('%d/%m/%Y %H:%M') if dt else '—'
        km_str = str(km) if km else '—'
        data.append([
            Paragraph(nome, cel),
            Paragraph(dt_str, cel),
            Paragraph(km_str, cel),
        ])

    t = Table(data, colWidths=[60*mm, 80*mm, 50*mm])
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
    elements.append(t)
    elements.append(Spacer(1, 2*mm))
    return elements


# ─── Página 2 ────────────────────────────────────────────────────────────────

def _fotos_marcos_grid(fotos_dict, marcos_lista, op=None):
    """Grid 5 colunas de fotos dos marcos."""
    elements = []
    elements.append(_section_header('FOTOS DOS MARCOS'))
    elements.append(Spacer(1, 1*mm))

    hdr_style = _s(7, bold=True, color=_BRANCO)
    data_style = _s(6, color='#1A1A1A')
    no_photo_style = _s(6, color=_CINZA_TXT)

    # Preparar dados de cada marco
    marcos_data = []
    for key, label in marcos_lista:
        url = fotos_dict.get(key)
        img = None
        if url:
            path = _os.path.join(settings.MEDIA_ROOT, url.replace('/media/', ''))
            if _os.path.exists(path):
                try:
                    img = Image(path)
                    if img.drawWidth <= 0 or img.drawHeight <= 0:
                        img = None
                    else:
                        ratio = min(35*mm / img.drawWidth, 25*mm / img.drawHeight, 1.0)
                        img.drawWidth *= ratio
                        img.drawHeight *= ratio
                        if img.drawWidth > 300*mm or img.drawHeight > 300*mm:
                            img = None
                except Exception:
                    logger.exception("Erro ao carregar foto marco %s", path)
                    img = None

        # Buscar data/km do marco operacional
        dt_str = '—'
        km_str = '—'
        if op:
            marco_map = {
                'inicio_viagem': (op.inicio_viagem, op.km_inicio_viagem),
                'chegada_operacao': (op.chegada_operacao, op.km_chegada_operacao),
                'inicio_operacao': (op.inicio_operacao, op.km_inicio_operacao),
                'termino_operacao': (op.termino_operacao, op.km_termino_operacao),
                'termino_viagem': (op.termino_viagem, op.km_termino_viagem),
            }
            dt, km = marco_map.get(key, (None, None))
            if dt:
                dt_str = dt.strftime('%d/%m/%Y %H:%M')
            if km:
                km_str = str(km)

        marcos_data.append((label, img, dt_str, km_str))

    # Cabeçalho da tabela
    header_row = [Paragraph(m[0], hdr_style) for m in marcos_data]

    # Linha de fotos
    photo_row = []
    for label, img, dt_str, km_str in marcos_data:
        if img:
            photo_row.append(img)
        else:
            photo_row.append(Paragraph('Sem foto', no_photo_style))

    # Linha de data/hora
    dt_row = [Paragraph(m[2], data_style) for m in marcos_data]

    # Linha de KM
    km_row = [Paragraph(f'KM: {m[3]}', data_style) if m[3] != '—' else Paragraph('—', data_style) for m in marcos_data]

    # Calcular tempo/distância entre marcos
    tempo_row = []
    if op:
        marcos_dt = [op.inicio_viagem, op.chegada_operacao, op.inicio_operacao, op.termino_operacao, op.termino_viagem]
        marcos_km = [op.km_inicio_viagem, op.km_chegada_operacao, op.km_inicio_operacao, op.km_termino_operacao, op.km_termino_viagem]
        for i in range(5):
            if i == 0:
                tempo_row.append(Paragraph('—', data_style))
            else:
                dt_prev, dt_cur = marcos_dt[i-1], marcos_dt[i]
                km_prev, km_cur = marcos_km[i-1], marcos_km[i]
                parts = []
                if dt_prev and dt_cur:
                    delta = abs((dt_cur - dt_prev).total_seconds())
                    parts.append(f'Tempo: {int(delta//3600):02d}:{int((delta%3600)//60):02d}')
                if km_prev and km_cur:
                    parts.append(f'Dist.: {km_cur - km_prev} km')
                tempo_row.append(Paragraph('<br/>'.join(parts) if parts else '—', data_style))
    else:
        tempo_row = [Paragraph('—', data_style)] * 5

    col_w = _W / 5
    table_data = [header_row, photo_row, dt_row, km_row, tempo_row]

    t = Table(table_data, colWidths=[col_w] * 5)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(_AZUL_HEADER)),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(_BRANCO)),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 3*mm))
    return elements


def _veiculos_table(veiculos):
    """Tabela de veículos escoltados."""
    if not veiculos:
        return []

    elements = []
    elements.append(_section_header('VEÍCULOS ESCOLTADOS'))
    elements.append(Spacer(1, 1*mm))

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(7, color='#1A1A1A')

    header = ['Nº', 'VEÍCULO', 'CAVALO', 'CARRETA', 'CARRETA 2', 'MOTORISTA']
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

    t = Table(data, colWidths=[12*mm, 40*mm, 30*mm, 30*mm, 30*mm, 48*mm])
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
    elements.append(t)
    elements.append(Spacer(1, 3*mm))
    return elements


def _fotos_veiculos_block(veiculos):
    """Fotos dos veículos escoltados (Antes da Escolta)."""
    elements = []

    for v in veiculos:
        fotos = list(v.fotos.all())
        if not fotos:
            continue

        placa = v.placa_cavalo or '—'
        motorista = v.motorista or '—'

        # Header da seção do veículo
        hdr_style = _s(7, bold=True, color=_BRANCO)
        hdr_data = [[Paragraph(f'FOTOS — {placa} · {motorista}', hdr_style)]]
        hdr = Table(hdr_data, colWidths=[_W])
        hdr.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor(_AZUL_MEDIO)),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        elements.append(hdr)
        elements.append(Spacer(1, 0.5*mm))

        # Subtítulo
        sub_style = _s(6, bold=True, color=_AZUL_MEDIO)
        elements.append(Paragraph('Antes da Escolta', sub_style))
        elements.append(Spacer(1, 0.5*mm))

        # Grid de fotos
        photo_row = []
        for foto in fotos:
            img = _img_field(foto.foto, max_w=55*mm, max_h=35*mm)
            if img:
                photo_row.append(img)
            else:
                photo_row.append('')

        if photo_row:
            # Preencher para múltiplo de 3
            while len(photo_row) % 3 != 0:
                photo_row.append('')
            n_cols = 3
            rows = [photo_row[i:i+n_cols] for i in range(0, len(photo_row), n_cols)]
            col_w = _W / n_cols
            t = Table(rows, colWidths=[col_w] * n_cols)
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#CCCCCC')),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            elements.append(t)

        elements.append(Spacer(1, 2*mm))

    return elements


def _rodape():
    """Rodapé fixo."""
    style = _s(8, bold=True, color=_AZUL_MEDIO, align=TA_CENTER)
    return [
        Spacer(1, 4*mm),
        Paragraph('ATENCIOSAMENTE — DEPARTAMENTO DE ESCOLTA ARMADA — JR SEGURANÇA', style),
    ]


# ─── Função principal ────────────────────────────────────────────────────────

def gerar_os_pdf(request, pk):
    """Gera PDF da OS no modelo compacto e retorna HttpResponse."""
    from .models import (
        OrdemServico, OSOperacional, FotoMarco,
        VeiculoEscoltado, FotoVeiculoEscoltado,
    )

    os_obj = OrdemServico.objects.select_related(
        'cliente', 'equipe', 'equipe__viatura',
        'equipe__agente1', 'equipe__agente2',
    ).get(pk=pk)

    op = getattr(os_obj, 'operacional', None)
    veiculos = list(os_obj.veiculos.order_by('ordem'))

    # Fotos dos marcos
    fotos_marco = {}
    for foto in FotoMarco.objects.filter(os=os_obj):
        fotos_marco[foto.marco] = foto.foto.url

    MARCOS_LISTA = [
        ('inicio_viagem',    'Início de Viagem'),
        ('chegada_operacao', 'Chegada Operação'),
        ('inicio_operacao',  'Início Operação'),
        ('termino_operacao', 'Término Operação'),
        ('termino_viagem',   'Término de Viagem'),
    ]

    # Dados dos agentes (snap + fallback via equipe)
    def _get_agente_data(snap_nome, snap_cpf, snap_rg, snap_tel, snap_cnh, snap_cnv, equipe_agente):
        """Retorna dados do agente: snap_* como primário, Agente como fallback."""
        nome = snap_nome or (equipe_agente.nome if equipe_agente else '—')
        cpf = snap_cpf or (equipe_agente.cpf if equipe_agente else '—')
        rg = snap_rg or (equipe_agente.rg if equipe_agente else '—')
        tel = snap_tel or (equipe_agente.telefone if equipe_agente else '—')
        cnh = snap_cnh or (equipe_agente.cnh if equipe_agente else '—')
        cnv = snap_cnv or (equipe_agente.cnv if equipe_agente else '—')
        val_cnh = '—'
        val_cnv = '—'
        endereco = '—'
        status = 'Ativo'
        if equipe_agente:
            if equipe_agente.cnh_validade:
                val_cnh = equipe_agente.cnh_validade.strftime('%d/%m/%Y')
            if equipe_agente.cnv_validade:
                val_cnv = equipe_agente.cnv_validade.strftime('%d/%m/%Y')
            if equipe_agente.endereco:
                endereco = equipe_agente.endereco
            status = dict(equipe_agente.STATUS_CHOICES).get(equipe_agente.status, equipe_agente.status)
        return nome, cpf, rg, tel, cnh, val_cnh, cnv, val_cnv, endereco, status

    ag1 = _get_agente_data(
        os_obj.snap_agente1_nome, os_obj.snap_agente1_cpf,
        os_obj.snap_agente1_rg, os_obj.snap_agente1_telefone,
        os_obj.snap_agente1_cnh, os_obj.snap_agente1_cnv,
        os_obj.equipe.agente1 if os_obj.equipe else None,
    )
    ag2 = _get_agente_data(
        os_obj.snap_agente2_nome, os_obj.snap_agente2_cpf,
        os_obj.snap_agente2_rg, os_obj.snap_agente2_telefone,
        os_obj.snap_agente2_cnh, os_obj.snap_agente2_cnv,
        os_obj.equipe.agente2 if os_obj.equipe else None,
    )

    # ── Montar PDF ───────────────────────────────────────────────────────
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=10*mm, rightMargin=10*mm,
        topMargin=10*mm, bottomMargin=10*mm,
        title=f'OS-{os_obj.numero}',
        author='JR Segurança',
    )

    elements = []

    # ── Página 1 ─────────────────────────────────────────────────────────
    elements.extend(_header_block(os_obj))
    elements.extend(_identificacao_os_block(os_obj))
    elements.extend(_trajeto_block(os_obj))
    elements.extend(_agente_block(1, *ag1))
    elements.extend(_agente_block(2, *ag2))
    elements.extend(_viatura_block(os_obj))
    elements.extend(_dados_operacao_block(op))

    # ── Página 2 ─────────────────────────────────────────────────────────
    elements.append(PageBreak())
    elements.extend(_fotos_marcos_grid(fotos_marco, MARCOS_LISTA, op))
    elements.extend(_veiculos_table(veiculos))
    elements.extend(_fotos_veiculos_block(veiculos))
    elements.extend(_rodape())

    # ── Build ────────────────────────────────────────────────────────────
    try:
        doc.build(elements)
    except Exception as e:
        logger.error("Erro ao gerar PDF da OS %s: %s", pk, e)
        # Retry sem imagens
        safe_elements = []
        for el in elements:
            if isinstance(el, Image):
                continue
            if isinstance(el, KeepTogether):
                safe_el = [x for x in el._content if not isinstance(x, Image)]
                if safe_el:
                    safe_elements.append(KeepTogether(safe_el))
            else:
                safe_elements.append(el)
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=10*mm, rightMargin=10*mm,
            topMargin=10*mm, bottomMargin=10*mm,
            title=f'OS-{os_obj.numero}',
            author='JR Segurança',
        )
        doc.build(safe_elements)
    buffer.seek(0)

    from django.http import FileResponse
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="OS-{os_obj.numero}.pdf"'
    return response
