import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
normal_style = ParagraphStyle('normal', parent=styles['Normal'], fontSize=7, leading=9)

def crea_tabella(df, titolo):
    elements = []
    titolo_style = ParagraphStyle('titolo', parent=styles['Heading2'], spaceAfter=10, alignment=0)
    if df.empty:
        elements.append(Paragraph(titolo, titolo_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("No values found", styles['Normal']))
        elements.append(Spacer(1, 12))
        return elements

    df = df.fillna("").astype(str)
    data = [[Paragraph(str(col), normal_style) for col in df.columns]]
    for _, row in df.iterrows():
        data.append([Paragraph(str(cell), normal_style) for cell in row])

    num_cols = len(df.columns)
    col_widths = [500 / num_cols] * num_cols

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    elements.append(Paragraph(titolo, titolo_style))
    elements.append(Spacer(1, 6))
    elements.append(table)
    elements.append(Spacer(1, 12))
    return elements

def genera_report(esn, base_dir):
    pdf_file = os.path.join(base_dir, f"Report_{esn}.pdf")
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, leftMargin=20, rightMargin=20)
    elements = []

    # Logo in alto a sinistra
    try:
        logo_path = os.path.join(base_dir, "logo.jpg")
        logo = Image(logo_path, width=100, height=40)
        elements.append(logo)
    except Exception:
        pass

    elements.append(Spacer(1, 20))
    # Titolo PDF modificato
    elements.append(Paragraph(f"Report for ESN {esn}", styles['Heading1']))
    elements.append(Spacer(1, 20))

    # --- Inserire qui la logica dei 3 database come prima ---
    # df_icss, df_thd, df_claim...
    # elements += crea_tabella(df_icss_risultato, titolo_icss)
    # elements += crea_tabella(df_thd_risultato, titolo_thd)
    # elements += crea_tabella(df_claim_risultato, titolo_claim)

    doc.build(elements)
    return pdf_file
