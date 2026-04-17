"""
cadastros/boletim_export.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sistema de Gestão de Escolta – DEMARK SEGURANÇA
Geração de Boletim de Medição em PDF e XLSX

Funções públicas:
    gerar_pdf_bytes(cliente, periodo, missoes, totais)  → bytes
    gerar_xlsx_bytes(cliente, periodo, missoes, totais) → bytes

Ambas são chamadas pelas views boletim_export_pdf e boletim_export_xlsx
definidas em views.py.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import io
from datetime import datetime

# ─── Identidade visual ───────────────────────────────────────────────────────
EMPRESA_NOME    = "DEMARK SEGURANÇA PRIVADA LTDA – DEPTO. DE ESCOLTA ARMADA"
SISTEMA_MODELO  = "BoletimMedicao.BoletimMedicao21"

# Paleta de cores (hex sem '#')
_AZUL_ESC  = "1A3A5C"
_AZUL_MED  = "2563A8"
_CINZA_CAB = "D0D8E4"
_CINZA_LIN = "F2F5F9"
_VERDE     = "217A3C"
_BRANCO    = "FFFFFF"
_FUNDO_HDR = "EBF2FA"
_FUNDO_TOT = "DBE8F5"
_CINZA_ROD = "888888"

# Definição das colunas: (título, largura relativa para PDF, largura em chars para XLSX)
# Estrutura conforme XLSX do usuário: Nº | O.S | Agentes | Origem | Destino | Viatura | Escoltado
# | Previsão Início | Chegada Operação | Início Operação | Término Operação
# | Total Horas | Franq Horas | Exced Horas | Total Km | Franq Km | Exced Km | Desloc
# | Hr Exc(R$) | Km Exc(R$) | Escolta(R$) | Desloc(R$) | Pedágio(R$) | TOTAL(R$)
_COLUNAS = [
    ("Nº",                  5,  5),
    ("O.S",                 9,  12),
    ("Agentes",            30,  35),
    ("Origem",             20,  20),
    ("Destino",            20,  20),
    ("Viatura",            10,  12),
    ("Escoltado",          10,  12),
    ("Previsão\nInício",  16,  18),
    ("Chegada\nOperação", 16,  18),
    ("Início\nOperação",  16,  18),
    ("Término\nOperação", 16,  18),
    ("Total\nHoras",      10,  10),
    ("Franq\nHoras",      10,  10),
    ("Exced\nHoras",      10,  10),
    ("Total\nKm",          9,  10),
    ("Franq\nKm",          9,  10),
    ("Exced\nKm",          9,  10),
    ("Desloc",              7,   8),
    ("Hr Exc\n(R$)",      11,  12),
    ("Km Exc\n(R$)",      11,  12),
    ("Escolta\n(R$)",     14,  14),
    ("Desloc\n(R$)",      11,  12),
    ("Pedágio\n(R$)",     11,  12),
    ("TOTAL\n(R$)",       14,  14),
]

# Índices (0-based) das colunas de valor monetário
_IDX_MOEDA = {18, 19, 20, 21, 22, 23}


# ─── Helpers ─────────────────────────────────────────────────────────────────

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
        m.get("n", ""),
        m.get("os", ""),
        m.get("agentes", "---"),
        m.get("origem", ""),
        m.get("destino", ""),
        m.get("viatura", "---"),
        m.get("escoltado", "---"),
        m.get("programada", ""),
        m.get("chegada", ""),
        m.get("inicio", ""),
        m.get("termino", ""),
        m.get("total_h", ""),
        m.get("franq_h", ""),
        m.get("exced_h", ""),
        m.get("total_km", 0),
        m.get("franq_km", 0),
        m.get("exced_km", 0),
        m.get("desloc", 0),
        m.get("hr_exc", 0.0),
        m.get("km_exc", 0.0),
        m.get("escolta", 0.0),
        m.get("desloc_val", 0.0),
        m.get("pedagio", 0.0),
        m.get("total", 0.0),
    ]


# ─── PDF ─────────────────────────────────────────────────────────────────────

def gerar_pdf_bytes(cliente: str, periodo: str, missoes: list, totais: dict) -> bytes:
    """Retorna o PDF do Boletim como bytes prontos para HttpResponse."""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

    c_azul  = colors.HexColor(f"#{_AZUL_ESC}")
    c_chdr  = colors.HexColor(f"#{_CINZA_CAB}")
    c_clin  = colors.HexColor(f"#{_CINZA_LIN}")
    c_verde = colors.HexColor(f"#{_VERDE}")
    c_fhdr  = colors.HexColor(f"#{_FUNDO_HDR}")
    c_ftot  = colors.HexColor(f"#{_FUNDO_TOT}")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                            leftMargin=8*mm, rightMargin=8*mm,
                            topMargin=8*mm, bottomMargin=8*mm)
    W = landscape(A4)[0] - 16*mm

    def _st(name, size=7, bold=False, align=TA_LEFT, color=colors.black, leading=9):
        return ParagraphStyle(name, fontSize=size,
                              fontName='Helvetica-Bold' if bold else 'Helvetica',
                              alignment=align, textColor=color, leading=leading)

    st_titulo  = _st('t1', 12, True,  TA_CENTER, c_azul, 14)
    st_empresa = _st('t2',  7, True,  TA_RIGHT,  c_azul,  9)
    st_cliente = _st('t3',  8, True,  TA_LEFT,   c_azul)
    st_cell    = _st('c1',  6, False, TA_LEFT,   colors.black, 7)
    st_cell_r  = _st('c2',  6, False, TA_RIGHT,  colors.black, 7)
    st_cell_bv = _st('c3',  6, True,  TA_RIGHT,  c_verde, 7)
    st_hdr_col = _st('h1',5.5, True,  TA_CENTER, c_azul,  6.5)
    st_tot_l   = _st('tl',5.5, True,  TA_LEFT,   c_azul,  7)
    st_tot_v   = _st('tv',5.5, True,  TA_RIGHT,  c_verde, 7)
    st_rodape  = _st('rd',  6, False, TA_CENTER, colors.HexColor(f"#{_CINZA_ROD}"))

    story = []
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    n_regs = totais.get("missoes", len(missoes))

    # Cabeçalho
    cab_data = [[
        Paragraph("<b>BOLETIM DE MEDIÇÃO</b>", st_titulo),
        Paragraph(
            f"<b>{EMPRESA_NOME}</b><br/>"
            f"Período: {periodo} – Total Registros: {n_regs:03d}",
            st_empresa),
    ]]
    t_cab = Table(cab_data, colWidths=[W * 0.55, W * 0.45])
    t_cab.setStyle(TableStyle([
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW',   (0,0), (-1,-1), 1, c_azul),
        ('BACKGROUND',  (0,0), (-1,-1), c_fhdr),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]))
    story.append(t_cab)
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(f"<b>Cliente: {cliente}</b>", st_cliente))
    story.append(Spacer(1, 2*mm))

    # Larguras proporcionais
    raw_w = [c[1] for c in _COLUNAS]
    col_w = [r * (W / sum(raw_w)) for r in raw_w]

    # Linha de cabeçalho
    header_row = [Paragraph(f"<b>{c[0]}</b>", st_hdr_col) for c in _COLUNAS]
    rows = [header_row]

    # Linhas de dados
    for m in missoes:
        vals = _missao_to_row(m)
        row = []
        for i, v in enumerate(vals):
            if i == 23:
                row.append(Paragraph(f"<b>{_fmt_brl(v)}</b>", st_cell_bv))
            elif i in _IDX_MOEDA:
                row.append(Paragraph(_fmt_brl(v), st_cell_r))
            elif i >= 13:
                row.append(Paragraph(str(v), st_cell_r))
            else:
                row.append(Paragraph(str(v), st_cell))
        rows.append(row)

    # Linha de totais
    _T = {
        0:  lambda: Paragraph(f"<b>TOTAL {totais.get('missoes','')} OS</b>", st_tot_l),
        11: lambda: Paragraph(f"<b>{totais.get('total_h','')}</b>",  st_tot_l),
        13: lambda: Paragraph(f"<b>{totais.get('exced_h','')}</b>",  st_tot_l),
        14: lambda: Paragraph(f"<b>{totais.get('total_km','')}</b>", st_tot_l),
        16: lambda: Paragraph(f"<b>{totais.get('exced_km','')}</b>", st_tot_l),
        17: lambda: Paragraph(f"<b>{totais.get('desloc_km','')}</b>",st_tot_l),
        18: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('hr_exc',0))}</b>",    st_tot_v),
        19: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('km_exc',0))}</b>",    st_tot_v),
        20: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('escolta',0))}</b>",   st_tot_v),
        21: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('desloc_val',0))}</b>",st_tot_v),
        22: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('pedagio',0))}</b>",   st_tot_v),
        23: lambda: Paragraph(f"<b>{_fmt_brl(totais.get('total',0))}</b>",     st_tot_v),
    }
    tot_row = [_T[i]() if i in _T else Paragraph("", st_tot_l) for i in range(len(_COLUNAS))]
    rows.append(tot_row)

    tabela = Table(rows, colWidths=col_w, repeatRows=1)
    style_cmds = [
        ('BACKGROUND',  (0,0),  (-1,0),  c_chdr),
        ('GRID',        (0,0),  (-1,-1), 0.3, colors.HexColor('#B0BBC8')),
        ('VALIGN',      (0,0),  (-1,-1), 'MIDDLE'),
        ('TOPPADDING',  (0,0),  (-1,-1), 2),
        ('BOTTOMPADDING',(0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0),  (-1,-1), 2),
        ('RIGHTPADDING',(0,0),  (-1,-1), 2),
        ('BACKGROUND',  (0,-1), (-1,-1), c_ftot),
        ('LINEABOVE',   (0,-1), (-1,-1), 1.2, c_azul),
    ]
    for i in range(1, len(rows) - 1):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), c_clin))
    tabela.setStyle(TableStyle(style_cmds))
    story.append(tabela)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        f"Gerado por: WMS | Modelo: {SISTEMA_MODELO} | Data: {data_geracao} | {EMPRESA_NOME}",
        st_rodape))

    doc.build(story)
    return buf.getvalue()


# ─── XLSX ────────────────────────────────────────────────────────────────────

def gerar_xlsx_bytes(cliente: str, periodo: str, missoes: list, totais: dict) -> bytes:
    """Retorna o XLSX do Boletim como bytes prontos para HttpResponse."""
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

    # ── L1: Título ─────────────────────────────────────────────────────────
    ws.merge_cells(f'A1:{last_col}1')
    ws['A1'] = "BOLETIM DE MEDIÇÃO"
    ws['A1'].font      = Font(name='Arial', bold=True, size=14, color=_AZUL_ESC)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws['A1'].fill      = _fill(_FUNDO_HDR)
    ws.row_dimensions[1].height = 24

    # ── L2: Empresa + Período ──────────────────────────────────────────────
    mid = n_cols // 2
    ws.merge_cells(f'A2:{get_column_letter(mid)}2')
    ws['A2'] = EMPRESA_NOME
    ws['A2'].font      = Font(name='Arial', bold=True, size=8, color=_AZUL_ESC)
    ws['A2'].alignment = Alignment(horizontal='left', vertical='center')
    ws['A2'].fill      = _fill(_FUNDO_HDR)

    c_per = get_column_letter(mid + 1)
    ws.merge_cells(f'{c_per}2:{last_col}2')
    ws[f'{c_per}2'] = f"Período: {periodo} – Total: {n_regs:03d} registros"
    ws[f'{c_per}2'].font      = Font(name='Arial', size=8, color=_AZUL_ESC)
    ws[f'{c_per}2'].alignment = Alignment(horizontal='right', vertical='center')
    ws[f'{c_per}2'].fill      = _fill(_FUNDO_HDR)
    ws.row_dimensions[2].height = 18

    # ── L3: Cliente ────────────────────────────────────────────────────────
    ws.merge_cells(f'A3:{last_col}3')
    ws['A3'] = f"Cliente: {cliente}"
    ws['A3'].font      = Font(name='Arial', bold=True, size=9, color=_AZUL_ESC)
    ws['A3'].alignment = Alignment(horizontal='left', vertical='center')
    ws['A3'].fill      = _fill(_FUNDO_HDR)
    ws.row_dimensions[3].height = 18

    # ── L4: Cabeçalho das colunas ──────────────────────────────────────────
    ROW_HDR = 4
    for ci, (col_name, _, col_w) in enumerate(_COLUNAS, start=1):
        cell = ws.cell(row=ROW_HDR, column=ci, value=col_name)
        cell.font      = Font(name='Arial', bold=True, size=8, color=_BRANCO)
        cell.fill      = _fill(_AZUL_ESC)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border    = _borda()
        ws.column_dimensions[get_column_letter(ci)].width = col_w
    ws.row_dimensions[ROW_HDR].height = 32

    # ── Dados ──────────────────────────────────────────────────────────────
    COLS_MOEDA_XL = {i + 1 for i in _IDX_MOEDA}  # 1-based
    # Colunas de horas (1-based): Total Horas=12, Franq Horas=13, Exced Horas=14
    COLS_HORAS_XL = {12, 13, 14}
    for ri, m in enumerate(missoes, start=ROW_HDR + 1):
        vals = _missao_to_row(m)
        bg   = _CINZA_LIN if ri % 2 == 0 else _BRANCO
        for ci, val in enumerate(vals, start=1):
            is_total = (ci == n_cols)  # last column = TOTAL (R$)
            # Horas devem ser gravadas como texto puro (evita interpretação timedelta)
            if ci in COLS_HORAS_XL:
                val = str(val) if val else '00:00'
            cell = ws.cell(row=ri, column=ci, value=val)
            if ci in COLS_HORAS_XL:
                cell.data_type = 's'  # força string
                cell.number_format = '@'
            cell.font   = Font(name='Arial', size=7, bold=is_total,
                               color=(_VERDE if is_total else "000000"))
            cell.fill   = _fill(bg)
            cell.border = _borda()
            cell.alignment = Alignment(
                horizontal='right' if ci >= 12 else 'left',
                vertical='center', wrap_text=(ci <= 4))
            if ci in COLS_MOEDA_XL:
                cell.number_format = '#,##0.00'
        ws.row_dimensions[ri].height = 22

    # ── Linha de totais ────────────────────────────────────────────────────
    ROW_TOT = ROW_HDR + 1 + len(missoes)
    tot_vals = [
        f"TOTAL MISSÕES: {totais.get('missoes','')}", '', '', '', '', '', '',
        '', '', '', '',
        totais.get('total_h',''), '', totais.get('exced_h',''),
        totais.get('total_km',''), '', totais.get('exced_km',''), totais.get('desloc_km',''),
        totais.get('hr_exc', 0),  totais.get('km_exc', 0),
        totais.get('escolta', 0), totais.get('desloc_val', 0),
        totais.get('pedagio', 0), totais.get('total', 0),
    ]
    for ci, val in enumerate(tot_vals, start=1):
        is_val = ci in COLS_MOEDA_XL
        if ci in COLS_HORAS_XL:
            val = str(val) if val else ''
        cell = ws.cell(row=ROW_TOT, column=ci, value=val)
        if ci in COLS_HORAS_XL:
            cell.data_type = 's'
            cell.number_format = '@'
        cell.font   = Font(name='Arial', bold=True, size=8,
                           color=(_VERDE if is_val else _AZUL_ESC))
        cell.fill   = _fill(_FUNDO_TOT)
        cell.border = _borda('medium')
        cell.alignment = Alignment(
            horizontal='right' if ci >= 12 else 'left', vertical='center')
        if ci in COLS_MOEDA_XL:
            cell.number_format = '#,##0.00'
    ws.row_dimensions[ROW_TOT].height = 20

    # ── Rodapé ─────────────────────────────────────────────────────────────
    ROW_ROD = ROW_TOT + 1
    ws.merge_cells(f'A{ROW_ROD}:{last_col}{ROW_ROD}')
    ws[f'A{ROW_ROD}'] = (
        f"Gerado por: WMS | Modelo: {SISTEMA_MODELO} | "
        f"Data: {data_geracao} | {EMPRESA_NOME}"
    )
    ws[f'A{ROW_ROD}'].font      = Font(name='Arial', size=7, italic=True, color=_CINZA_ROD)
    ws[f'A{ROW_ROD}'].alignment = Alignment(horizontal='center')

    ws.freeze_panes = 'A5'

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
