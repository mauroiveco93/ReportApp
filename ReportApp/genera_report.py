import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
normal_style = ParagraphStyle('normal', parent=styles['Normal'], fontSize=7, leading=9)

def create_table(df, title):
    elements = []
    title_style = ParagraphStyle('title', parent=styles['Heading2'], spaceAfter=10, alignment=0)

    if df.empty:
        elements.append(Paragraph(title, title_style))
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

    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 6))
    elements.append(table)
    elements.append(Spacer(1, 12))
    return elements

def genera_report(esn, base_dir):
    pdf_file = os.path.join(base_dir, f"Report_{esn}.pdf")
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, leftMargin=20, rightMargin=20)
    elements = []

    # --- Logo a sinistra ---
    try:
        logo_path = os.path.join(base_dir, "logo.jpg")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=100, height=40)
            header = Table([[logo, ""]], colWidths=[100, 400])
            elements.append(header)
    except Exception:
        pass  # se il logo manca, si continua senza

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Report for ESN {esn}", styles['Heading1']))
    elements.append(Spacer(1, 20))

    # --- ICSS ---
    service_path = os.path.join(base_dir, "data", "Data Base Service.xlsx")
    df_icss = pd.read_excel(service_path)
    df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_icss_filtrato.empty:
        df_icss_filtrato['WAT_ORIGINAL'] = pd.to_datetime(df_icss_filtrato['WAT_ORIGINAL'], errors='coerce')
        df_icss_filtrato = df_icss_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
        title_icss = f"ICSS Dossiers - {len(df_icss_filtrato)}"
        df_icss_result = df_icss_filtrato[[
            "DOSSIER ID", "WAT_ORIGINAL", "DEALER", "Engine Serial Number",
            "Pre-diagnosis", "Repair Description"
        ]]
    else:
        title_icss = "ICSS Dossiers - 0"
        df_icss_result = pd.DataFrame()
    elements += create_table(df_icss_result, title_icss)

    # --- THD ---
    thd_path = os.path.join(base_dir, "data", "THD FM.xlsx")
    df_thd = pd.read_excel(thd_path)
    df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_thd_filtrato.empty:
        df_thd_filtrato['Submitted On'] = pd.to_datetime(df_thd_filtrato['Submitted On'], errors='coerce')
        df_thd_filtrato = df_thd_filtrato.sort_values("Submitted On", ascending=False)
        title_thd = f"THD - {len(df_thd_filtrato)}"
        df_thd_result = df_thd_filtrato[[
            "Request/Report Number","Submitted On","Request/Report Subtype","Dealer",
            "Question","Symptom","Solution","Status Reason","Product Type"
        ]]
    else:
        title_thd = "THD - 0"
        df_thd_result = pd.DataFrame()
    elements += create_table(df_thd_result, title_thd)

    # --- Claims ---
    claim_path = os.path.join(base_dir, "data", "Data Base Warranty.xlsx")
    df_claim = pd.read_excel(claim_path)
    df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
    if not df_claim_filtrato.empty:
        df_claim_filtrato['Claim Payment Date'] = pd.to_datetime(df_claim_filtrato['Claim Payment Date'], errors='coerce')
        df_claim_filtrato = df_claim_filtrato.sort_values("Claim Payment Date", ascending=False)
        total_amount = df_claim_filtrato["Approved Amount"].sum()
        currency = df_claim_filtrato["Local Currency Code"].iloc[0] if "Local Currency Code" in df_claim_filtrato.columns else ""
        title_claim = f"Claims - Total {total_amount:.2f} {currency}"
        df_claim_result = df_claim_filtrato[[
            "FPT Engine Family","Claim Number","Payed Dealer Name",
            "Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"
        ]]
    else:
        title_claim = "Claims - Total 0"
        df_claim_result = pd.DataFrame()
    elements += create_table(df_claim_result, title_claim)

    doc.build(elements)
    return pdf_file
