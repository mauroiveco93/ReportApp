import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

styles = getSampleStyleSheet()
normal_style = ParagraphStyle('normal', parent=styles['Normal'], fontSize=7, leading=9)

def crea_tabella(df, titolo):
    elements = []
    titolo_style = ParagraphStyle('title', parent=styles['Heading2'], spaceAfter=10, alignment=0)

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
    col_widths = [900 / num_cols] * num_cols  # adattiamo la larghezza

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

def genera_report(esn, base_dir="."):
    try:
        pdf_file = os.path.join(base_dir, f"Report_{esn}.pdf")
        doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4), leftMargin=20, rightMargin=20)
        elements = []

        # Logo a sinistra
        logo_path = os.path.join(base_dir, "logo.jpg")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=120, height=50)
            header = Table([[logo, Paragraph("Engine Report", styles['Title'])]], colWidths=[130, 700])
            elements.append(header)
        else:
            elements.append(Paragraph("Engine Report", styles['Title']))

        elements.append(Spacer(1, 20))

        # --- Dossier ICSS ---
        df_icss = pd.read_excel(os.path.join(base_dir, "data", "Data Base Service.xlsx"))
        df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
        if not df_icss_filtrato.empty:
            df_icss_filtrato['WAT_ORIGINAL'] = pd.to_datetime(df_icss_filtrato['WAT_ORIGINAL'], errors='coerce')
            df_icss_filtrato = df_icss_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
            titolo_icss = f"Dossier ICSS - {len(df_icss_filtrato)}"
            df_icss_risultato = df_icss_filtrato[["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"]]
        else:
            titolo_icss = "Dossier ICSS - 0"
            df_icss_risultato = pd.DataFrame()
        elements += crea_tabella(df_icss_risultato, titolo_icss)

        # --- THD ---
        df_thd = pd.read_excel(os.path.join(base_dir, "data", "THD FM.xlsx"))
        df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
        if not df_thd_filtrato.empty:
            df_thd_filtrato['Submitted On'] = pd.to_datetime(df_thd_filtrato['Submitted On'], errors='coerce')
            df_thd_filtrato = df_thd_filtrato.sort_values("Submitted On", ascending=False)
            titolo_thd = f"THD - {len(df_thd_filtrato)}"
            df_thd_risultato = df_thd_filtrato[["Request/Report Number","Submitted On","Request/Report Subtype","Dealer","Question","Symptom","Solution","Status Reason","Product Type"]]
        else:
            titolo_thd = "THD - 0"
            df_thd_risultato = pd.DataFrame()
        elements += crea_tabella(df_thd_risultato, titolo_thd)

        # --- Claim ---
        df_claim = pd.read_excel(os.path.join(base_dir, "data", "Data Base Warranty.xlsx"))
        df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
        if not df_claim_filtrato.empty:
            df_claim_filtrato['Claim Payment Date'] = pd.to_datetime(df_claim_filtrato['Claim Payment Date'], errors='coerce')
            df_claim_filtrato = df_claim_filtrato.sort_values("Claim Payment Date", ascending=False)
            total_amount = df_claim_filtrato["Approved Amount"].sum()
            currency = df_claim_filtrato["Local Currency Code"].iloc[0] if "Local Currency Code" in df_claim_filtrato.columns else ""
            titolo_claim = f"Claim - Total {total_amount:.2f} {currency}"
            df_claim_risultato = df_claim_filtrato[["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"]]
        else:
            titolo_claim = "Claim - Total 0"
            df_claim_risultato = pd.DataFrame()
        elements += crea_tabella(df_claim_risultato, titolo_claim)

        doc.build(elements)
        return pdf_file
    except Exception as e:
        raise RuntimeError(f"Error generating PDF: {e}")
