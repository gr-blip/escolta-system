"""
cadastros/pdf_processo.py
━━━━━━━━━━━━━━━━━━━━━━━━━
Geração de PDF completo para Consulta de Processos judiciais (DriverID).

Retorna BytesIO com o PDF pronto para salvar no model ou enviar como response.
"""

import io
from datetime import datetime


def gerar_pdf_consulta(consulta_processo) -> io.BytesIO:
    """
    Gera PDF com todos os dados da consulta de processos judiciais.

    Args:
        consulta_processo: instância de ConsultaProcesso

    Returns:
        BytesIO com o PDF gerado.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    )
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm)

    styles = getSampleStyleSheet()

    # Cores
    AZUL     = colors.HexColor('#1A3A5C')
    AZUL_CLR = colors.HexColor('#1F4E79')
    VERDE    = colors.HexColor('#16a34a')
    VERMELHO = colors.HexColor('#dc2626')
    AMBAR    = colors.HexColor('#eab308')
    CINZA    = colors.HexColor('#6b7280')
    FUNDO    = colors.HexColor('#f7f7f5')

    # Estilos
    s_titulo = ParagraphStyle('titulo', parent=styles['Title'],
                               fontSize=14, textColor=AZUL, spaceAfter=4)
    s_sub    = ParagraphStyle('sub', parent=styles['Normal'],
                               fontSize=9, textColor=CINZA, alignment=TA_CENTER)
    s_label  = ParagraphStyle('label', parent=styles['Normal'],
                               fontSize=7, textColor=CINZA, spaceAfter=1)
    s_valor  = ParagraphStyle('valor', parent=styles['Normal'],
                               fontSize=9, textColor=colors.black, spaceAfter=6)
    s_card   = ParagraphStyle('card', parent=styles['Normal'],
                               fontSize=8, textColor=colors.black, leading=11)
    s_card_b = ParagraphStyle('card_bold', parent=s_card,
                               fontSize=9, textColor=AZUL)
    s_small  = ParagraphStyle('small', parent=styles['Normal'],
                               fontSize=7, textColor=CINZA)

    elements = []

    # ── Cabeçalho ───────────────────────────────────────────────────────────
    elements.append(Paragraph("JR SEGURANÇA E VIGILÂNCIA PATRIMONIAL LTDA", s_titulo))
    elements.append(Paragraph("Relatório de Consulta de Processos Judiciais — DriverID", s_sub))
    elements.append(Spacer(1, 4*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=AZUL))
    elements.append(Spacer(1, 4*mm))

    # ── Dados do funcionário ────────────────────────────────────────────────
    func = consulta_processo.funcionario
    dados_func = [
        [Paragraph("Funcionário", s_label), Paragraph(func.nome, s_valor),
         Paragraph("CPF", s_label), Paragraph(func.cpf, s_valor)],
        [Paragraph("Status CPF", s_label),
         Paragraph(consulta_processo.status_cpf or '—', s_valor),
         Paragraph("Tipo", s_label),
         Paragraph(func.get_tipo_display(), s_valor)],
        [Paragraph("Data da consulta", s_label),
         Paragraph(consulta_processo.criado_em.strftime('%d/%m/%Y %H:%M'), s_valor),
         Paragraph("Total de processos", s_label),
         Paragraph(str(consulta_processo.total_processos), s_valor)],
    ]
    t_func = Table(dados_func, colWidths=[25*mm, 55*mm, 25*mm, 55*mm])
    t_func.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(t_func)
    elements.append(Spacer(1, 6*mm))

    # ── Processos ───────────────────────────────────────────────────────────
    processos = consulta_processo.resultado_json.get('data', {}).get('data', [])
    if not processos:
        # fallback: processos básicos do result
        res = consulta_processo.resultado_json.get('data', {}).get('result', {})
        processos = res.get('processos', [])

    if not processos:
        elements.append(Paragraph("Nenhum processo encontrado para este CPF.", s_valor))
    else:
        elements.append(Paragraph(
            f"Processos encontrados: <b>{len(processos)}</b>",
            ParagraphStyle('cnt', parent=s_valor, fontSize=10, textColor=AZUL)
        ))
        elements.append(Spacer(1, 3*mm))

        for i, proc in enumerate(processos, 1):
            # Cabeçalho do processo
            num = proc.get('process_number', proc.get('numero', f'#{i}'))
            tribunal = proc.get('court', proc.get('tribunal', '—'))
            uf = proc.get('state', proc.get('uf', ''))
            ramo = proc.get('law_branch', proc.get('area', '—'))
            status_proc = proc.get('process_status', proc.get('statusObservacao', '—'))

            # Cor do badge por ramo
            ramo_lower = ramo.lower() if ramo else ''
            if 'penal' in ramo_lower or 'criminal' in ramo_lower:
                ramo_cor = VERMELHO
            elif 'civil' in ramo_lower or 'cível' in ramo_lower:
                ramo_cor = colors.HexColor('#2563eb')
            elif 'trabalh' in ramo_lower:
                ramo_cor = colors.HexColor('#7c3aed')
            elif 'administr' in ramo_lower:
                ramo_cor = colors.HexColor('#0891b2')
            else:
                ramo_cor = CINZA

            elements.append(HRFlowable(width="100%", thickness=0.3, color=CINZA))
            elements.append(Spacer(1, 2*mm))

            header_data = [[
                Paragraph(f"<b>Processo {i}</b>", s_card_b),
                Paragraph(f"Nº: <b>{num}</b>", s_card),
                Paragraph(f"Tribunal: <b>{tribunal}</b> {uf}", s_card),
            ]]
            t_hdr = Table(header_data, colWidths=[30*mm, 60*mm, 70*mm])
            t_hdr.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, -1), FUNDO),
                ('ROUNDEDCORNERS', [3, 3, 3, 3]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(t_hdr)
            elements.append(Spacer(1, 2*mm))

            # Dados do processo
            classe = proc.get('procedural_class', proc.get('classeProcessual', {}).get('nome', '—') if isinstance(proc.get('classeProcessual'), dict) else proc.get('classeProcessual', '—'))
            data_aut = proc.get('filing_date', proc.get('dataAutuacao', '—'))
            if isinstance(data_aut, str) and 'T' in data_aut:
                try:
                    data_aut = datetime.fromisoformat(data_aut.replace('Z', '+00:00')).strftime('%d/%m/%Y')
                except Exception:
                    pass
            valor = proc.get('claim_value', '—')
            seg = proc.get('segment', proc.get('area', '—'))
            org_julg = proc.get('judging_body', '—')

            proc_info = [
                [Paragraph("Classe", s_label), Paragraph(str(classe), s_card),
                 Paragraph("Ramo", s_label),
                 Paragraph(f'<font color="#{ramo_cor.hexval()[2:]}">{ramo}</font>', s_card)],
                [Paragraph("Data autuação", s_label), Paragraph(str(data_aut), s_card),
                 Paragraph("Status", s_label), Paragraph(str(status_proc), s_card)],
                [Paragraph("Segmento", s_label), Paragraph(str(seg), s_card),
                 Paragraph("Órgão julgador", s_label), Paragraph(str(org_julg), s_card)],
                [Paragraph("Valor causa", s_label),
                 Paragraph(f'R$ {valor:,.2f}' if isinstance(valor, (int, float)) else str(valor), s_card),
                 Paragraph("Justiça gratuita", s_label),
                 Paragraph('Sim' if proc.get('free_justice') else 'Não', s_card)],
            ]
            t_info = Table(proc_info, colWidths=[22*mm, 58*mm, 22*mm, 58*mm])
            t_info.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            elements.append(t_info)

            # Partes
            partes = proc.get('parties', proc.get('partes', []))
            if partes:
                elements.append(Spacer(1, 1*mm))
                elements.append(Paragraph("<b>Partes:</b>", s_card))
                for p in partes:
                    nome_p = p.get('name', p.get('nome', '—'))
                    papel = p.get('role', p.get('papel', '—'))
                    lado = p.get('side', p.get('lado', ''))
                    elements.append(Paragraph(
                        f"• {nome_p} — {papel} ({lado})" if lado else f"• {nome_p} — {papel}",
                        s_card
                    ))

            # Assuntos
            assuntos = proc.get('subjects', proc.get('assuntosCNJ', []))
            if assuntos:
                elements.append(Spacer(1, 1*mm))
                elements.append(Paragraph("<b>Assuntos:</b>", s_card))
                for a in assuntos:
                    titulo_a = a.get('subject_title', a.get('titulo', '—'))
                    prim = ' (principal)' if a.get('is_primary', a.get('principal')) else ''
                    elements.append(Paragraph(f"• {titulo_a}{prim}", s_card))

            elements.append(Spacer(1, 4*mm))

    # ── Rodapé ──────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 6*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=AZUL))
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph(
        f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} — JR Segurança © {datetime.now().year}",
        ParagraphStyle('rodape', parent=s_small, alignment=TA_CENTER)
    ))

    doc.build(elements)
    buf.seek(0)
    return buf
