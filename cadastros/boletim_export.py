"""
cadastros/boletim_export.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sistema de Gestão de Escolta  JR SEGURANÇA
Geração de Boletim de Medição em PDF e XLSX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import io
from datetime import datetime

EMPRESA_NOME   = "JR SEGURANÇA"
SISTEMA_MODELO = "BoletimMedicao.BoletimMedicao21"

_AZUL_ESC  = "1A3A5C"
_CINZA_CAB = "D0D8E4"
_CINZA_LIN = "F2F5F9"
_VERDE     = "217A3C"
_BRANCO    = "FFFFFF"
_FUNDO_HDR = "EBF2FA"
_FUNDO_TOT = "DBE8F5"
_CINZA_ROD = "888888"
_AMARELO   = "F5A623"   # destaque TOTAL (R$) — igual ao modelo Excel

# ─── Definição de colunas ────────────────────────────────────────────────────
# (título, largura_PDF_pts, largura_XLSX_chars)
# ATENÇÃO: a soma das larguras PDF deve respeitar a largura total da página.
# A4 landscape = 841.89 pt; margens 8mm cada lado → W ≈ 809 pt.
# Coloque os valores absolutos em pontos; o código fará o scaling proporcional.
_COLUNAS = [
    ("Nº",                          18,   5),
    ("O.S",                         28,   8),
    ("Agentes",                     80,  22),
    ("Origem",                      52,  18),
    ("Destino",                     52,  18),
    ("Viatura",                     30,  12),
    ("Escoltado",                   36,  14),
    ("Previsão de\nInício",         38,  16),
    ("Chegada\nOperação",           38,  16),
    ("Início de\nOperação",         38,  16),
    ("Término\nOperação",           38,  16),
    ("Total\nHoras",                28,   9),
    ("Franq\nHoras",                28,   9),
    ("Exced\nHoras",                28,   9),
    ("Total\nKm",                   26,   9),
    ("Franq\nKm",                   26,   9),
    ("Exced\nKm",                   26,   9),
    ("Desloc",                      22,   8),
    ("Hr Exc\n(R$)",                30,  11),
    ("Km Exc\n(R$)",                30,  11),
    ("Escolta\n(R$)",               38,  14),
    ("Desloc\n(R$)",                30,  11),
    ("Pedágio\n(R$)",               30,  11),
    ("TOTAL\n(R$)",                 40,  14),
]

# índices 0-based das colunas monetárias
_IDX_MOEDA = {18, 19, 20, 21, 22, 23}


def _fmt_brl(valor) -> str:
    try:
        v = float(valor)
    except (TypeError, ValueError):
        v = 0.0
    if v == 0:
        return "0,00"
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _missao_to_row(m: dict) -> list:
    return [
        m.get("n", ""),             # 0  Nº
        m.get("os", ""),            # 1  O.S
        m.get("agentes", ""),       # 2  Agentes
        m.get("origem", ""),        # 3  Origem
        m.get("destino", ""),       # 4  Destino
        m.get("viatura", ""),       # 5  Viatura
        m.get("escoltado", "---"),  # 6  Escoltado
        m.get("programada", ""),    # 7  Previsão de Início
        m.get("chegada", ""),       # 8  Chegada Operação
        m.get("inicio", ""),        # 9  Início de Operação
        m.get("termino", ""),       # 10 Término Operação
        m.get("total_h", ""),       # 11 Total Horas
        m.get("franq_h", ""),       # 12 Franq Horas
        m.get("exced_h", ""),       # 13 Exced Horas
        m.get("total_km", 0),       # 14 Total Km
        m.get("franq_km", 0),       # 15 Franq Km
        m.get("exced_km", 0),       # 16 Exced Km
        m.get("desloc", 0),         # 17 Desloc
        m.get("hr_exc", 0.0),       # 18 Hr Exc (R$)
        m.get("km_exc", 0.0),       # 19 Km Exc (R$)
        m.get("escolta", 0.0),      # 20 Escolta (R$)
        m.get("desloc_val", 0.0),   # 21 Desloc (R$)
        m.get("pedagio", 0.0),      # 22 Pedágio (R$)
        m.get("total", 0.0),        # 23 TOTAL (R$)
    ]


# ─── PDF ─────────────────────────────────────────────────────────────────────

def gerar_pdf_bytes(cliente: str, periodo: str, missoes: list, totais: dict) -> bytes:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

    c_azul   = colors.HexColor(f"#{_AZUL_ESC}")
    c_verde  = colors.HexColor(f"#{_VERDE}")
    c_fhdr   = colors.HexColor(f"#{_FUNDO_HDR}")
    c_ftot   = colors.HexColor(f"#{_FUNDO_TOT}")
    c_clin   = colors.HexColor(f"#{_CINZA_LIN}")
    c_cinza  = colors.HexColor(f"#{_CINZA_CAB}")
    c_amar   = colors.HexColor(f"#{_AMARELO}")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=landscape(A4),
        leftMargin=8*mm, rightMargin=8*mm,
        topMargin=8*mm, bottomMargin=10*mm,
    )
    W = landscape(A4)[0] - 16*mm  # largura útil ≈ 809 pt

    # ── Estilos de parágrafo ────────────────────────────────────────────────
    def _st(name, size=7, bold=False, align=TA_LEFT, color=colors.black, leading=None):
        return ParagraphStyle(
            name,
            fontSize=size,
            fontName='Helvetica-Bold' if bold else 'Helvetica',
            alignment=align,
            textColor=color,
            leading=leading or (size + 1.5),
        )

    st_titulo  = _st('t1', 13, True,  TA_CENTER, c_azul)
    st_empresa = _st('t2',  7, True,  TA_RIGHT,  c_azul)
    st_per     = _st('t3',  6, False, TA_RIGHT,  c_azul)
    st_cliente = _st('t4',  8, True,  TA_LEFT,   c_azul)
    st_emitido = _st('t5',  6, False, TA_RIGHT,  colors.HexColor(f"#{_CINZA_ROD}"))

    st_hdr     = _st('h1',  6, True,  TA_CENTER, colors.white)
    st_cel_l   = _st('c1',  6, False, TA_LEFT,   colors.black)
    st_cel_r   = _st('c2',  6, False, TA_RIGHT,  colors.black)
    st_cel_v   = _st('c3',  6, True,  TA_RIGHT,  c_verde)    # excedente verde
    st_cel_tot = _st('c4',  7, True,  TA_RIGHT,  c_azul)     # TOTAL (R$) negrito azul
    st_tot_l   = _st('tl',  6, True,  TA_LEFT,   c_azul)
    st_tot_v   = _st('tv',  6, True,  TA_RIGHT,  c_verde)
    st_rodape  = _st('rd',  5, False, TA_CENTER, colors.HexColor(f"#{_CINZA_ROD}"))

    story = []
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    n_regs = totais.get("missoes", len(missoes))

    # ── Cabeçalho superior ──────────────────────────────────────────────────
    cab_data = [[
        Paragraph("<b>BOLETIM DE MEDIÇÃO</b>", st_titulo),
        Paragraph(
            f"<b>Período: {periodo}</b>  |  <b>Total: {n_regs:03d} registro(s)</b><br/>"
            f"{EMPRESA_NOME}",
            st_empresa
        ),
    ]]
    t_cab = Table(cab_data, colWidths=[W * 0.50, W * 0.50])
    t_cab.setStyle(TableStyle([
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND',   (0, 0), (-1, -1), c_azul),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (0, -1), 8),
        ('RIGHTPADDING', (1, 0), (1, -1), 8),
    ]))
    # Corrige cor do texto do título para branco no fundo azul
    st_titulo_branco = _st('t1b', 13, True, TA_CENTER, colors.white)
    st_empresa_branco = _st('t2b', 7, True, TA_RIGHT, colors.white)
    cab_data[0][0] = Paragraph("<b>BOLETIM DE MEDIÇÃO</b>", st_titulo_branco)
    cab_data[0][1] = Paragraph(
        f"<b>Período: {periodo}</b>  |  <b>Total: {n_regs:03d} registro(s)</b><br/>"
        f"{EMPRESA_NOME}",
        st_empresa_branco
    )
    t_cab = Table(cab_data, colWidths=[W * 0.50, W * 0.50])
    t_cab.setStyle(TableStyle([
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND',   (0, 0), (-1, -1), c_azul),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (0, -1), 8),
        ('RIGHTPADDING', (1, 0), (1, -1), 8),
    ]))
    story.append(t_cab)

    # ── Linha cliente + emitido em ──────────────────────────────────────────
    cli_data = [[
        Paragraph(f"<b>Cliente:  {cliente}</b>", st_cliente),
        Paragraph(f"Emitido em: {data_geracao}", st_emitido),
    ]]
    t_cli = Table(cli_data, colWidths=[W * 0.6, W * 0.4])
    t_cli.setStyle(TableStyle([
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND',   (0, 0), (-1, -1), c_fhdr),
        ('TOPPADDING',   (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 3),
        ('LEFTPADDING',  (0, 0), (0, -1), 6),
        ('RIGHTPADDING', (1, 0), (1, -1), 6),
        ('LINEBELOW',    (0, 0), (-1, -1), 0.5, c_azul),
    ]))
    story.append(t_cli)
    story.append(Spacer(1, 2*mm))

    # ── Larguras das colunas (proporcional à soma total) ────────────────────
    raw_w  = [c[1] for c in _COLUNAS]
    total_w = sum(raw_w)
    col_w  = [r * (W / total_w) for r in raw_w]

    # ── Linha de cabeçalho das colunas ─────────────────────────────────────
    header_row = [Paragraph(f"<b>{c[0]}</b>", st_hdr) for c in _COLUNAS]
    rows = [header_row]

    # ── Linhas de dados ─────────────────────────────────────────────────────
    for m in missoes:
        vals = _missao_to_row(m)
        row = []
        for i, v in enumerate(vals):
            if i == 23:
                # TOTAL (R$) — negrito, azul
                row.append(Paragraph(f"<b>{_fmt_brl(v)}</b>", st_cel_tot))
            elif i in _IDX_MOEDA:
                # valores monetários à direita
                row.append(Paragraph(_fmt_brl(v), st_cel_r))
            elif i in {11, 12, 13, 14, 15, 16, 17}:
                # números/horas à direita
                row.append(Paragraph(str(v), st_cel_r))
            elif i == 13:
                # excedente horas em verde
                row.append(Paragraph(str(v), st_cel_v))
            else:
                row.append(Paragraph(str(v), st_cel_l))
        rows.append(row)

    # ── Linha de totais ─────────────────────────────────────────────────────
    _T = {
        0:  lambda: Paragraph(f"<b>TOTAL: {totais.get('missoes','')} O.S</b>", st_tot_l),
        11: lambda: Paragraph(f"<b>{totais.get('total_h','')}</b>",   st_tot_v),
        13: lambda: Paragraph(f"<b>{totais.get('exced_h','')}</b>",   st_tot_v),
        14: lambda: Paragraph(f"<b>{totais.get('total_km','')}</b>",  st_tot_l),
        16: lambda: Paragraph(f"<b>{totais.get('exced_km','')}</b>",  st_tot_v),
        17: lambda: Paragraph(f"<b>{totais.get('desloc_km','')}</b>", st_tot_l),
        18: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('hr_exc',0))}</b>",     st_tot_v),
        19: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('km_exc',0))}</b>",     st_tot_v),
        20: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('escolta',0))}</b>",    st_tot_v),
        21: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('desloc_val',0))}</b>", st_tot_v),
        22: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('pedagio',0))}</b>",    st_tot_v),
        23: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('total',0))}</b>",      st_tot_v),
    }
    tot_row = [_T[i]() if i in _T else Paragraph("", st_tot_l) for i in range(len(_COLUNAS))]
    rows.append(tot_row)

    # ── Tabela principal ─────────────────────────────────────────────────────
    tabela = Table(rows, colWidths=col_w, repeatRows=1)

    style_cmds = [
        # Cabeçalho
        ('BACKGROUND',    (0, 0),  (-1, 0),  c_azul),
        ('TEXTCOLOR',     (0, 0),  (-1, 0),  colors.white),
        ('TOPPADDING',    (0, 0),  (-1, 0),  4),
        ('BOTTOMPADDING', (0, 0),  (-1, 0),  4),

        # Grid geral
        ('GRID',          (0, 0),  (-1, -1), 0.3, colors.HexColor('#B0BBC8')),
        ('VALIGN',        (0, 0),  (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 1),  (-1, -1), 2),
        ('BOTTOMPADDING', (0, 1),  (-1, -1), 2),
        ('LEFTPADDING',   (0, 0),  (-1, -1), 3),
        ('RIGHTPADDING',  (0, 0),  (-1, -1), 3),

        # Linha de totais
        ('BACKGROUND',    (0, -1), (-1, -1), c_ftot),
        ('LINEABOVE',     (0, -1), (-1, -1), 1.2, c_azul),
        ('TOPPADDING',    (0, -1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 3),

        # Destaque coluna TOTAL (R$)
        ('BACKGROUND',    (23, 1), (23, -2), colors.HexColor('#FFF3CD')),
        ('BACKGROUND',    (23, -1),(23, -1), c_amar),
    ]

    # Linhas alternadas
    for i in range(1, len(rows) - 1):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (22, i), c_clin))

    tabela.setStyle(TableStyle(style_cmds))
    story.append(tabela)
    story.append(Spacer(1, 3*mm))

    # ── Rodapé ──────────────────────────────────────────────────────────────
    story.append(Paragraph(
        f"Gerado por: WMS  ·  Modelo: {SISTEMA_MODELO}  ·  "
        f"Data: {data_geracao}  ·  {EMPRESA_NOME}",
        st_rodape,
    ))

    doc.build(story)
    return buf.getvalue()


# ─── XLSX ────────────────────────────────────────────────────────────────────

def gerar_xlsx_bytes(cliente: str, periodo: str, missoes: list, totais: dict) -> bytes:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Boletim de Medição"

    def _borda(tipo='thin'):
        s = Side(style=tipo, color='B0BBC8')
        return Border(left=s, right=s, top=s, bottom=s)

    def _fill(hex_color):
        return PatternFill('solid', fgColor=hex_color)

    n_cols   = len(_COLUNAS)
    last_col = get_column_letter(n_cols)
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    n_regs = totais.get("missoes", len(missoes))

    # L1: Título
    ws.merge_cells(f'A1:{last_col}1')
    ws['A1'] = "BOLETIM DE MEDIÇÃO"
    ws['A1'].font      = Font(name='Arial', bold=True, size=14, color=_BRANCO)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws['A1'].fill      = _fill(_AZUL_ESC)
    ws.row_dimensions[1].height = 26

    # L2: Empresa (esq) + Período (dir)
    mid = n_cols // 2
    ws.merge_cells(f'A2:{get_column_letter(mid)}2')
    ws['A2'] = f"Período: {periodo}  |  Total: {n_regs:03d} registro(s)"
    ws['A2'].font      = Font(name='Arial', bold=True, size=8, color=_BRANCO)
    ws['A2'].alignment = Alignment(horizontal='left', vertical='center')
    ws['A2'].fill      = _fill(_AZUL_ESC)

    c_per = get_column_letter(mid + 1)
    ws.merge_cells(f'{c_per}2:{last_col}2')
    ws[f'{c_per}2'] = EMPRESA_NOME
    ws[f'{c_per}2'].font      = Font(name='Arial', bold=True, size=8, color=_BRANCO)
    ws[f'{c_per}2'].alignment = Alignment(horizontal='right', vertical='center')
    ws[f'{c_per}2'].fill      = _fill(_AZUL_ESC)
    ws.row_dimensions[2].height = 18

    # L3: Cliente + emitido
    ws.merge_cells(f'A3:{get_column_letter(mid)}3')
    ws['A3'] = f"Cliente: {cliente}"
    ws['A3'].font      = Font(name='Arial', bold=True, size=9, color=_AZUL_ESC)
    ws['A3'].alignment = Alignment(horizontal='left', vertical='center')
    ws['A3'].fill      = _fill(_FUNDO_HDR)

    ws.merge_cells(f'{c_per}3:{last_col}3')
    ws[f'{c_per}3'] = f"Emitido em: {data_geracao}"
    ws[f'{c_per}3'].font      = Font(name='Arial', size=8, color=_CINZA_ROD)
    ws[f'{c_per}3'].alignment = Alignment(horizontal='right', vertical='center')
    ws[f'{c_per}3'].fill      = _fill(_FUNDO_HDR)
    ws.row_dimensions[3].height = 18

    # L4: Cabeçalho das colunas
    ROW_HDR = 4
    for ci, (col_name, _, col_w) in enumerate(_COLUNAS, start=1):
        cell = ws.cell(row=ROW_HDR, column=ci, value=col_name)
        cell.font      = Font(name='Arial', bold=True, size=8, color=_BRANCO)
        cell.fill      = _fill(_AZUL_ESC)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border    = _borda()
        ws.column_dimensions[get_column_letter(ci)].width = col_w
    ws.row_dimensions[ROW_HDR].height = 32

    # Dados
    COLS_MOEDA_XL = {i + 1 for i in _IDX_MOEDA}
    for ri, m in enumerate(missoes, start=ROW_HDR + 1):
        vals = _missao_to_row(m)
        bg   = _CINZA_LIN if ri % 2 == 0 else _BRANCO
        for ci, val in enumerate(vals, start=1):
            is_total = (ci == n_cols)
            cell = ws.cell(row=ri, column=ci, value=val)
            cell.font   = Font(
                name='Arial', size=7, bold=is_total,
                color=(_AZUL_ESC if is_total else "000000"),
            )
            cell.fill   = _fill("FFF3CD" if is_total else bg)
            cell.border = _borda()
            cell.alignment = Alignment(
                horizontal='right' if ci >= 12 else 'left',
                vertical='center',
                wrap_text=(ci <= 7),
            )
            if ci in COLS_MOEDA_XL:
                cell.number_format = '#,##0.00'
        ws.row_dimensions[ri].height = 22

    # Linha de totais
    ROW_TOT = ROW_HDR + 1 + len(missoes)
    tot_vals = [
        f"TOTAL: {totais.get('missoes','')} O.S",  # 1  Nº
        '', '', '', '', '', '',                      # 2-7
        '', '', '', '',                              # 8-11
        totais.get('total_h', ''),                   # 12 Total Horas
        '',                                          # 13 Franq Horas
        totais.get('exced_h', ''),                   # 14 Exced Horas
        totais.get('total_km', ''),                  # 15 Total Km
        '',                                          # 16 Franq Km
        totais.get('exced_km', ''),                  # 17 Exced Km
        totais.get('desloc_km', ''),                 # 18 Desloc
        totais.get('hr_exc',    0),                  # 19 Hr Exc (R$)
        totais.get('km_exc',    0),                  # 20 Km Exc (R$)
        totais.get('escolta',   0),                  # 21 Escolta (R$)
        totais.get('desloc_val',0),                  # 22 Desloc (R$)
        totais.get('pedagio',   0),                  # 23 Pedágio (R$)
        totais.get('total',     0),                  # 24 TOTAL (R$)
    ]
    for ci, val in enumerate(tot_vals, start=1):
        is_val = ci in COLS_MOEDA_XL
        is_total_col = (ci == n_cols)
        cell = ws.cell(row=ROW_TOT, column=ci, value=val)
        cell.font   = Font(
            name='Arial', bold=True, size=8,
            color=(_VERDE if is_val else _AZUL_ESC),
        )
        cell.fill   = _fill(_AMARELO if is_total_col else _FUNDO_TOT)
        cell.border = _borda('medium')
        cell.alignment = Alignment(
            horizontal='right' if ci >= 12 else 'left',
            vertical='center',
        )
        if ci in COLS_MOEDA_XL:
            cell.number_format = '#,##0.00'
    ws.row_dimensions[ROW_TOT].height = 22

    # Rodapé
    ROW_ROD = ROW_TOT + 1
    ws.merge_cells(f'A{ROW_ROD}:{last_col}{ROW_ROD}')
    ws[f'A{ROW_ROD}'] = (
        f"Gerado por: WMS  ·  Modelo: {SISTEMA_MODELO}  ·  "
        f"Data: {data_geracao}  ·  {EMPRESA_NOME}"
    )
    ws[f'A{ROW_ROD}'].font      = Font(name='Arial', size=7, italic=True, color=_CINZA_ROD)
    ws[f'A{ROW_ROD}'].alignment = Alignment(horizontal='center')
    ws.row_dimensions[ROW_ROD].height = 14

    ws.freeze_panes = 'A5'

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()

