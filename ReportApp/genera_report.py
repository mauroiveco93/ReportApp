import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def genera_report(esn, output_path, base_dir):
    try:
        # Percorsi file
        service_file = os.path.join(base_dir, "data", "Data Base Service.xlsx")
        thd_file = os.path.join(base_dir, "data", "THD FM.xlsx")
        warranty_file = os.path.join(base_dir, "data", "Data Base Warranty.xlsx")

        # Carica i dati
        df_service = pd.read_excel(service_file)
        df_thd = pd.read_excel(thd_file)
        df_warranty = pd.read_excel(warranty_file)

        # Filtra per ESN
        service_data = df_service[df_service['ESN'] == esn]
        thd_data = df_thd[df_thd['ESN'] == esn]
        warranty_data = df_warranty[df_warranty['ESN'] == esn]

        # Crea PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Logo
        logo_path = os.path.join(base_dir, "logo.jpg")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=80, height=40)
            elements.append(logo)

        # Titolo
        elements.append(Paragraph("Engine Report", styles['Title']))
        elements.append(Spacer(1, 20))

        # Tabelle
        for title, df in [("Service Data", service_data), ("THD Data", thd_data), ("Warranty Data", warranty_data)]:
            if not df.empty:
                elements.append(Paragraph(title, styles['Heading2']))
                table_data = [df.columns.tolist()] + df.values.tolist()
                table = Table(table_data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 15))

        doc.build(elements)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Errore nella generazione del report: {e}")
