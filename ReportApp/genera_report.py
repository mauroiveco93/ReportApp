import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def genera_report(esn):
    # ====== Percorsi relativi ======
    BASE_DIR = os.path.dirname(__file__)
    file_icss = os.path.join(BASE_DIR, "Data Base Service.xlsx")
    file_thd = os.path.join(BASE_DIR, "THD FM.xlsx")
    file_claim = os.path.join(BASE_DIR, "Data Base Warranty.xlsx")
    logo_path = os.path.join(BASE_DIR, "logo.jpg")

    # ====== Caricamento dati ======
    df_icss = pd.read_excel(file_icss)
    df_thd = pd.read_excel(file_thd, dtype={"Engine Serial Number": str})
    df_claim = pd.read_excel(file_claim, dtype={"FPT Serial Number Customer": str})

    # ====== Filtra ICSS ======
    df_icss_filtrato = df_icss[df_icss["Engine Serial Number"] == esn]
    if not df_icss_filtrato.empty:
        df_icss_filtrato = df_icss_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
        titolo_icss = f"Dossier ICSS - {len(df_icss_filtrato)}"
        df_icss_risultato = df_icss_filtrato[["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"]]
    else:
        titolo_icss = "Dossier ICSS - 0"
        df_icss_risultato = pd.DataFrame(columns=["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"])

    # ====== Filtra THD ======
    df_thd_filtrato = df_thd[df_thd["Engine Serial Number"] == esn]
    if not df_thd_filtrato.empty:
        df_thd_filtrato = df_thd_filtrato.sort_values("Submitted On", ascending=False)
        titolo_thd = f"THD - {len(df_thd_filtrato)}"
        df_thd_risultato = df_thd_filtrato[["Request/Report Number", "Submitted On", "Request/Report Subtype",
                                            "Dealer", "Question", "Symptom", "Solution", "Status Reason", "Product Type"]]
    else:
        titolo_thd = "THD - 0"
        df_thd_risultato = pd.DataFrame(columns=["Request/Report Number", "Submitted On", "Request/Report Subtype",
                                                "Dealer", "Question", "Symptom", "Solution", "Status Reason", "Product Type"])

    # ====== Filtra Claim ======
    df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"] == esn]
    if not df_claim_filtrato.empty:
        df_claim_filtrato = df_claim_filtrato.sort_values("Claim Payment Date", ascending=False)
        claim_total_amount = df_claim_filtrato["Approved Amount"].sum()
        claim_currency = df_claim_filtrato["Local Currency Code"].iloc[0] if not df_claim_filtrato.empty else ""
        titolo_claim = f"Claim - Total {claim_total_amount:.2f} {claim_currency}"
        df_claim_risultato = df_claim_filtrato[["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"]]
    else:
        titolo_claim = "Claim - Total 0"
        df_claim_risultato = pd.DataFrame(columns=["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"])

    # ====== Creazione PDF ======
    pdf_file = os.path.join(BASE_DIR, f"Report_{esn}.pdf")
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    # Logo
    if os.path.exists(logo_path):
        img = Image(logo_path, width=150, height=50)  # dimensione fissa
        elements.append(img)
        elements.append(Spacer(1, 12))

    # Titolo generale
    elements.append(Paragraph(f"Report ESN {esn}", styles['Title']))
    elements.append(Spacer(1, 12))

    # ====== Funzione per creare tabelle ======
    def crea_tabella(df, titolo):
        elems = []
        elems.append(Paragraph(titolo, styles['Heading2']))
        elems.append(Spacer(1, 6))

        if df.empty:
            elems.append(Paragraph("No values found", styles['Normal']))
        else:
            data = [list(df.columns)] + df.values.tolist()
            t = Table(data, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR',(0,0),(-1,0),colors.black),
                ('ALIGN',(0,0),(-1,-1),'LEFT'),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            elems.append(t)
        elems.append(Spacer(1, 12))
        return elems

    # Aggiungi tutte le tabelle
    elements += crea_tabella(df_icss_risultato, titolo_icss)
    elements += crea_tabella(df_thd_risultato, titolo_thd)
    elements += crea_tabella(df_claim_risultato, titolo_claim)

    # Build PDF
    doc.build(elements)

    return f"Report_{esn}.pdf"
