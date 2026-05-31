"""
cadastros/os_pdf.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ordem de Serviço — PDF profissional (A4 landscape)
Layout: 2 páginas — identificação, marcos, fotos, veículos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import io
import logging
import os as _os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, HRFlowable, KeepTogether, PageBreak,
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


def _fmt_dt(dt, fmt='%d/%m/%Y %H:%M'):
    """Formata datetime convertendo UTC→local (America/Sao_Paulo)."""
    if not dt:
        return '—'
    from django.utils import timezone
    if dt.tzinfo:
        dt = timezone.localtime(dt)
    return dt.strftime(fmt)


def _safe_file_path(field):
    """Retorna o path absoluto de um ImageField, ou None."""
    try:
        if field and hasattr(field, 'path') and _os.path.exists(field.path):
            return field.path
    except Exception:
        pass
    return None


def _img_field(field, max_w=50 * mm, max_h=35 * mm):
    """Cria um flowable Image de um ImageField, ou None."""
    path = _safe_file_path(field)
    if not path:
        return None
    try:
        img = Image(path)
        if img.drawWidth <= 0 or img.drawHeight <= 0:
            logger.warning("Image %s: dimensões inválidas %sx%s", path, img.drawWidth, img.drawHeight)
            return None
        ratio = min(max_w / img.drawWidth, max_h / img.drawHeight, 1.0)
        img.drawWidth *= ratio
        img.drawHeight *= ratio
        if img.drawWidth > 300 * mm or img.drawHeight > 300 * mm:
            logger.warning("Image %s: dimensões pós-escala %sx%s pts", path, img.drawWidth, img.drawHeight)
            return None
        return img
    except Exception:
        logger.exception("Erro ao carregar imagem %s", path)
        return None


def _section_header(title):
    """Header de seção — faixa azul com texto branco."""
    style = ParagraphStyle(
        'sec_hdr', parent=getSampleStyleSheet()['Normal'],
        fontSize=9, leading=11,
        fontName='Helvetica-Bold',
        textColor=HexColor(_BRANCO),
    )
    data = [[Paragraph(title, style)]]
    t = Table(data, colWidths=[277 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(_AZUL_HEADER)),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


def _info_table(rows, col_widths=None):
    """Tabela de informações label:valor com bordas sutis."""
    if not rows:
        return []
    label_s = _s(7, bold=True, color=_CINZA_TXT)
    value_s = _s(8, color='#1A1A1A')

    data = []
    for row in rows:
        r = []
        for i, cell in enumerate(row):
            if i % 2 == 0:
                r.append(Paragraph(cell, label_s))
            else:
                r.append(Paragraph(str(cell) if cell else '—', value_s))
        data.append(r)

    if col_widths is None:
        col_widths = [30 * mm, 60 * mm, 30 * mm, 60 * mm, 30 * mm, 67 * mm]
    # Ajustar para número de colunas da primeira linha
    n_cols = len(data[0]) if data else 6
    if len(col_widths) != n_cols:
        col_widths = [277 * mm / n_cols] * n_cols

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor(_BRANCO), HexColor(_CINZA_BG)]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return [t]


# ─── Página 1 — Blocos ──────────────────────────────────────────────────────


def _header_block(os_obj):
    """Cabeçalho: JR SEGURANÇA + OS + Status."""
    elements = []
    s_logo = ParagraphStyle(
        'logo', parent=getSampleStyleSheet()['Normal'],
        fontSize=16, leading=18, fontName='Helvetica-Bold',
        textColor=HexColor(_AZUL_DEST),
    )
    s_os = ParagraphStyle(
        'os_num', parent=getSampleStyleSheet()['Normal'],
        fontSize=12, leading=14, fontName='Helvetica-Bold',
        textColor=HexColor(_BRANCO), alignment=TA_RIGHT,
    )
    s_status = ParagraphStyle(
        'status', parent=getSampleStyleSheet()['Normal'],
        fontSize=9, leading=11, fontName='Helvetica-Bold',
        textColor=HexColor(_BRANCO), alignment=TA_RIGHT,
    )

    status_display = os_obj.get_status_display()
    status_color = {
        'aberta': _VERDE, 'em_viagem': _AZUL_DEST,
        'em_operacao': _LARANJA, 'encerrando': _LARANJA,
        'concluida': _VERDE, 'finalizada': _CINZA_TXT,
        'cancelada': _VERMELHO,
    }.get(os_obj.status, _CINZA_TXT)

    logo_p = Paragraph('JR SEGURANÇA', s_logo)
    os_p = Paragraph(f'OS-{os_obj.numero}', s_os)
    status_p = Paragraph(status_display, ParagraphStyle(
        'st_badge', parent=getSampleStyleSheet()['Normal'],
        fontSize=9, leading=11, fontName='Helvetica-Bold',
        textColor=HexColor(_BRANCO), alignment=TA_CENTER,
    ))

    # Status badge
    badge_data = [[status_p]]
    badge = Table(badge_data, colWidths=[25 * mm])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(status_color)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    header_data = [[logo_p, os_p, badge]]
    header = Table(header_data, colWidths=[120 * mm, 110 * mm, 27 * mm])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor(_AZUL_ESCURO)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(header)
    elements.append(Spacer(1, 3 * mm))
    return elements


def _identificacao_os_block(os_obj):
    """Seção: Identificação da OS."""
    elements = []
    elements.append(_section_header('IDENTIFICAÇÃO DA OS'))
    elements.append(Spacer(1, 1 * mm))

    folha = ''
    try:
        folha = os_obj.operacional.numero_folha or ''
    except Exception:
        pass

    rows = [
        ['Nº OS / FOLHA', f'{os_obj.numero} / {folha}' if folha else os_obj.numero,
         'TIPO DE OPERAÇÃO', os_obj.get_tipo_viagem_display(),
         'STATUS', os_obj.get_status_display()],
        ['EMPRESA CONTRATANTE', os_obj.cliente.razao_social if os_obj.cliente else '—',
         'SOLICITANTE', os_obj.solicitante or '—', '', ''],
        ['DATA INÍCIO', _fmt_dt(os_obj.previsao_inicio, '%d/%m/%Y'),
         'HORA INÍCIO', _fmt_dt(os_obj.previsao_inicio, '%H:%M'),
         'TEL / CONTATO', getattr(os_obj, 'telefone_contato', '') or '—'],
        ['FORMA SOLICITAÇÃO', os_obj.get_forma_solicitacao_display(), '', '', '', ''],
    ]
    elements.extend(_info_table(rows))
    elements.append(Spacer(1, 3 * mm))
    return elements


def _trajeto_block(os_obj):
    """Seção: Trajeto / Rota."""
    elements = []
    elements.append(_section_header('TRAJETO / ROTA'))
    elements.append(Spacer(1, 1 * mm))

    rows = [
        ['CIDADE ORIGEM', os_obj.cidade_origem or '—', 'UF', os_obj.uf_origem or '—',
         'CIDADE DESTINO', os_obj.cidade_destino or '—', 'UF', os_obj.uf_destino or '—'],
    ]
    # 8 colunas
    cw = [28 * mm, 55 * mm, 12 * mm, 15 * mm, 28 * mm, 55 * mm, 12 * mm, 15 * mm]
    elements.extend(_info_table(rows, col_widths=cw))
    elements.append(Spacer(1, 3 * mm))
    return elements


def _agent_block(num, nome, cpf, rg, telefone, cnh, val_cnh, cnv, val_cnv, endereco, status='Ativo'):
    """Bloco de identificação de agente."""
    elements = []
    elements.append(_section_header(f'IDENTIFICAÇÃO DO AGENTE {num}'))
    elements.append(Spacer(1, 1 * mm))

    val_cnh_str = val_cnh.strftime('%d/%m/%Y') if val_cnh else '—'
    val_cnv_str = val_cnv.strftime('%d/%m/%Y') if val_cnv else '—'

    # Badge de status
    status_s = _s(7, bold=True, color=_BRANCO, align=TA_CENTER)
    st_color = _VERDE if status and status.lower() in ('ativo', 'at') else _VERMELHO

    rows1 = [
        ['NOME COMPLETO', nome or '—', 'CPF', cpf or '—',
         'RG', rg or '—', 'CONTATO', telefone or '—'],
        ['CNH', cnh or '—', 'VAL. CNH', val_cnh_str,
         'CNV', cnv or '—', 'VAL. CNV', val_cnv_str],
    ]
    rows2 = [
        ['ENDEREÇO', endereco or '—'],
    ]

    # 8 colunas para dados do agente
    cw8 = [18 * mm, 50 * mm, 14 * mm, 35 * mm, 14 * mm, 35 * mm, 18 * mm, 35 * mm]
    elements.extend(_info_table(rows1, col_widths=cw8))

    # Endereço (largura total)
    cw_end = [28 * mm, 249 * mm]
    elements.extend(_info_table(rows2, col_widths=cw_end))
    elements.append(Spacer(1, 2 * mm))
    return elements


def _viatura_block(modelo, cor, frota, placa, renavan, mct):
    """Bloco de identificação da viatura."""
    elements = []
    elements.append(_section_header('VIATURA'))
    elements.append(Spacer(1, 1 * mm))

    rows = [
        ['MODELO', modelo or '—', 'COR', cor or '—',
         'FROTA', frota or '—', 'PLACA', placa or '—'],
        ['RENAVAN', renavan or '—', 'MCT / ID', mct or '—', '', '', '', ''],
    ]
    cw = [18 * mm, 50 * mm, 14 * mm, 35 * mm, 14 * mm, 35 * mm, 18 * mm, 35 * mm]
    elements.extend(_info_table(rows, col_widths=cw))
    elements.append(Spacer(1, 3 * mm))
    return elements


def _dados_operacao_block(os_obj):
    """Tabela de marcos da operação."""
    elements = []
    elements.append(_section_header('DADOS DA OPERAÇÃO'))
    elements.append(Spacer(1, 1 * mm))

    hdr = _s(7, bold=True, color=_BRANCO)
    cel = _s(7, color='#1A1A1A')
    cel_bold = _s(7, bold=True, color='#1A1A1A')

    header = ['MARCO', 'DATA / HORA', 'KM']
    data = [[Paragraph(h, hdr) for h in header]]

    try:
        op = os_obj.operacional
    except Exception:
        op = None

    marcos = [
        ('Previsão de Início', os_obj.previsao_inicio, None),
        ('Início de Viagem', getattr(op, 'inicio_viagem', None), getattr(op, 'km_inicio_viagem', None)),
        ('Chegada Operação', getattr(op, 'chegada_operacao', None), getattr(op, 'km_chegada_operacao', None)),
        ('Início Operação', getattr(op, 'inicio_operacao', None), getattr(op, 'km_inicio_operacao', None)),
        ('Término Operação', getattr(op, 'termino_operacao', None), getattr(op, 'km_termino_operacao', None)),
        ('Término de Viagem', getattr(op, 'termino_viagem', None), getattr(op, 'km_termino_viagem', None)),
    ]

    for nome_marco, dt, km in marcos:
        dt_str = _fmt_dt(dt)
        km_str = str(km) if km else '—'
        data.append([
            Paragraph(nome_marco, cel_bold),
            Paragraph(dt_str, cel),
            Paragraph(km_str, cel),
        ])

    t = Table(data, colWidths=[70 * mm, 130 * mm, 77 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(_AZUL_HEADER)),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(_BRANCO)),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor(_BRANCO), HexColor(_CINZA_BG)]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t)
    return elements


# ─── Página 2 — Blocos ──────────────────────────────────────────────────────


def _fotos_marcos_block(os_obj):
    """Grid de fotos dos marcos (5 colunas)."""
    elements = []
    elements.append(_section_header('FOTOS DOS MARCOS'))
    elements.append(Spacer(1, 2 * mm))

    from .models import FotoMarco
    fotos_qs = FotoMarco.objects.filter(os=os_obj)
    fotos_dict = {}
    for f in fotos_qs:
        if f.marco not in fotos_dict:
            fotos_dict[f.marco] = f

    try:
        op = os_obj.operacional
    except Exception:
        op = None

    marcos_info = [
        ('inicio_viagem',    'Início de Viagem',    getattr(op, 'inicio_viagem', None),    getattr(op, 'km_inicio_viagem', None)),
        ('chegada_operacao', 'Chegada Operação',     getattr(op, 'chegada_operacao', None), getattr(op, 'km_chegada_operacao', None)),
        ('inicio_operacao',  'Início Operação',      getattr(op, 'inicio_operacao', None),  getattr(op, 'km_inicio_operacao', None)),
        ('termino_operacao', 'Término Operação',     getattr(op, 'termino_operacao', None), getattr(op, 'km_termino_operacao', None)),
        ('termino_viagem',   'Término de Viagem',    getattr(op, 'termino_viagem', None),   getattr(op, 'km_termino_viagem', None)),
    ]

    cap_s = ParagraphStyle(
        'cap', parent=getSampleStyleSheet()['Normal'],
        fontSize=6, leading=7.5, fontName='Helvetica',
        textColor=HexColor(_CINZA_TXT), alignment=TA_CENTER,
    )
    no_foto_s = ParagraphStyle(
        'no_foto', parent=getSampleStyleSheet()['Normal'],
        fontSize=7, leading=9, fontName='Helvetica-Oblique',
        textColor=HexColor('#AAAAAA'), alignment=TA_CENTER,
    )

    row_cells = []
    for key, label, dt, km in marcos_info:
        foto = fotos_dict.get(key)
        dt_str = _fmt_dt(dt)
        km_str = f'KM: {km}' if km else ''

        if foto and foto.foto:
            img = _img_field(foto.foto, max_w=50 * mm, max_h=30 * mm)
            if img:
                cell_content = [img]
            else:
                cell_content = [Paragraph('Sem foto', no_foto_s)]
        else:
            cell_content = [Paragraph('Sem foto', no_foto_s)]

        cell_content.append(Paragraph(dt_str, cap_s))
        if km_str:
            cell_content.append(Paragraph(km_str, cap_s))
        row_cells.append(cell_content)

    # Tabela 1 linha x 5 colunas
    foto_w = 55 * mm
    t = Table([row_cells], colWidths=[foto_w] * 5)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 4 * mm))
    return elements


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

    t = Table(data, colWidths=[12 * mm, 55 * mm, 40 * mm, 40 * mm, 40 * mm, 55 * mm])
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


def _fotos_veiculos_block(veiculos):
    """Fotos dos veículos escoltados (Antes/Após)."""
    from .models import FotoVeiculoEscoltado
    elements = []

    for v in veiculos:
        fotos = FotoVeiculoEscoltado.objects.filter(veiculo=v)
        if not fotos:
            continue

        label = f'{v.placa_cavalo or "—"} · {v.motorista or "—"}'
        elements.append(Paragraph(
            f'FOTOS — {label}',
            _s(8, bold=True, color=_AZUL_MEDIO)
        ))
        elements.append(Spacer(1, 1 * mm))

        # Agrupar por momento
        for momento_key, momento_label in [('antes', 'Antes da Escolta'), ('depois', 'Após a Escolta')]:
            fotos_m = [f for f in fotos if f.momento == momento_key]
            if not fotos_m:
                continue

            elements.append(Paragraph(momento_label, _s(7, bold=True, color=_CINZA_TXT)))
            row = []
            for foto in fotos_m[:4]:
                img = _img_field(foto.foto, max_w=60 * mm, max_h=35 * mm)
                if img:
                    row.append([img])
            if row:
                cw = [68 * mm] * len(row)
                t = Table([row], colWidths=cw)
                t.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#DDDDDD')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 3),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ]))
                elements.append(t)
            elements.append(Spacer(1, 2 * mm))

        elements.append(Spacer(1, 2 * mm))

    return elements


# ─── View principal ──────────────────────────────────────────────────────────


def gerar_os_pdf(request, pk):
    """Gera o PDF da OS com layout de 2 páginas."""
    from .models import (
        OrdemServico, OSOperacional, FotoMarco, AssinaturaOS,
        VeiculoEscoltado, FotoVeiculoEscoltado,
    )

    os_obj = OrdemServico.objects.select_related(
        'cliente', 'equipe', 'equipe__agente1', 'equipe__agente2',
        'equipe__viatura',
    ).get(pk=pk)

    try:
        os_obj.operacional
    except Exception:
        pass

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=10 * mm, rightMargin=10 * mm,
        topMargin=10 * mm, bottomMargin=10 * mm,
        title=f'OS-{os_obj.numero}',
        author='JR Segurança',
    )

    # ── Página 1 ──
    elements = []
    elements.extend(_header_block(os_obj))
    elements.extend(_identificacao_os_block(os_obj))
    elements.extend(_trajeto_block(os_obj))

    # Agentes (fallback para modelo se snap não populado — OS antigas)
    eq = getattr(os_obj, 'equipe', None)
    a1 = getattr(eq, 'agente1', None) if eq else None
    a2 = getattr(eq, 'agente2', None) if eq else None
    viat = getattr(eq, 'viatura', None) if eq else None

    ag1_fields = [
        os_obj.snap_agente1_nome or (a1.nome if a1 else ''),
        os_obj.snap_agente1_cpf or (a1.cpf if a1 else ''),
        os_obj.snap_agente1_rg or (a1.rg if a1 else ''),
        os_obj.snap_agente1_telefone or (a1.telefone if a1 else ''),
        os_obj.snap_agente1_cnh or (a1.cnh if a1 else ''),
        os_obj.snap_agente1_val_cnh or (getattr(a1, 'cnh_validade', None) if a1 else None),
        os_obj.snap_agente1_cnv or (a1.cnv if a1 else ''),
        os_obj.snap_agente1_val_cnv or (getattr(a1, 'cnv_validade', None) if a1 else None),
        os_obj.snap_agente1_endereco or (getattr(a1, 'endereco', '') if a1 else ''),
    ]
    elements.extend(_agent_block(1, *ag1_fields))

    if os_obj.snap_agente2_nome or a2:
        ag2_fields = [
            os_obj.snap_agente2_nome or (a2.nome if a2 else ''),
            os_obj.snap_agente2_cpf or (a2.cpf if a2 else ''),
            os_obj.snap_agente2_rg or (a2.rg if a2 else ''),
            os_obj.snap_agente2_telefone or (a2.telefone if a2 else ''),
            os_obj.snap_agente2_cnh or (a2.cnh if a2 else ''),
            os_obj.snap_agente2_val_cnh or (getattr(a2, 'cnh_validade', None) if a2 else None),
            os_obj.snap_agente2_cnv or (a2.cnv if a2 else ''),
            os_obj.snap_agente2_val_cnv or (getattr(a2, 'cnv_validade', None) if a2 else None),
            os_obj.snap_agente2_endereco or (getattr(a2, 'endereco', '') if a2 else ''),
        ]
        elements.extend(_agent_block(2, *ag2_fields))

    # Viatura (fallback)
    elements.extend(_viatura_block(
        os_obj.snap_viatura_modelo or (viat.marca_modelo if viat else ''),
        os_obj.snap_viatura_cor or (viat.cor if viat else ''),
        os_obj.snap_viatura_frota or (viat.frota if viat else ''),
        os_obj.snap_viatura_placa or (viat.placa if viat else ''),
        os_obj.snap_viatura_renavan or (viat.renavam if viat else ''),
        os_obj.snap_viatura_mct or (viat.mct_id if viat else ''),
    ))

    # Dados da Operação
    elements.extend(_dados_operacao_block(os_obj))

    # ── Página 2 ──
    elements.append(PageBreak())

    # Fotos dos marcos
    elements.extend(_fotos_marcos_block(os_obj))

    # Veículos escoltados
    veiculos = list(VeiculoEscoltado.objects.filter(os=os_obj))
    if veiculos:
        elements.append(_section_header('VEÍCULOS ESCOLTADOS'))
        elements.append(Spacer(1, 2 * mm))
        elements.extend(_veiculos_table(veiculos))
        elements.append(Spacer(1, 4 * mm))

        # Fotos dos veículos
        elements.extend(_fotos_veiculos_block(veiculos))

    # Rodapé
    elements.append(Spacer(1, 6 * mm))
    elements.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#CCCCCC')))
    elements.append(Spacer(1, 2 * mm))
    from django.utils import timezone as _tz
    now_str = _tz.localtime(_tz.now()).strftime('%d/%m/%Y %H:%M')
    footer_style = _s(7, color=_CINZA_TXT, align=TA_CENTER)
    elements.append(Paragraph(
        f'ATENCIOSAMENTE — DEPARTAMENTO DE ESCOLTA ARMADA — JR SEGURANÇA | '
        f'Gerado em {now_str}',
        footer_style
    ))

    # ── Build ──
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
            elif isinstance(el, Table):
                safe_elements.append(el)
            else:
                safe_elements.append(el)
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            leftMargin=10 * mm, rightMargin=10 * mm,
            topMargin=10 * mm, bottomMargin=10 * mm,
            title=f'OS-{os_obj.numero}',
            author='JR Segurança',
        )
        doc.build(safe_elements)
    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="OS-{os_obj.numero}.pdf"'
    return response
