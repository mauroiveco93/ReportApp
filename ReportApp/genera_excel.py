# genera_excel.py
import os
import pandas as pd
from io import BytesIO

def genera_excel(esn, base_dir="."):
    """
    Genera un file Excel con le stesse informazioni del PDF.
    - esn: Engine Serial Number inserito dall'utente
    - base_dir: cartella in cui sono presenti i file Excel
    Ritorna: BytesIO del file Excel pronto per lo scarico in Streamlit
    """
    try:
        # Percorsi ai file
        icss_file = os.path.join(base_dir, "Data Base Service.xlsx")
        thd_file = os.path.join(base_dir, "THD FM.xlsx")
        claim_file = os.path.join(base_dir, "Data Base Warranty.xlsx")

        # Lettura file
        df_icss = pd.read_excel(icss_file)
        df_thd = pd.read_excel(thd_file)
        df_claim = pd.read_excel(claim_file)

        # --- Filtri per ESN ---
        # ICSS
        df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
        if not df_icss_filtrato.empty:
            df_icss_filtrato['WAT_ORIGINAL'] = pd.to_datetime(df_icss_filtrato['WAT_ORIGINAL'], errors='coerce')
            df_icss_filtrato = df_icss_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
            df_icss_risultato = df_icss_filtrato[["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"]]
        else:
            df_icss_risultato = pd.DataFrame(columns=["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"])

        # THD
        df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
        if not df_thd_filtrato.empty:
            df_thd_filtrato['Submitted On'] = pd.to_datetime(df_thd_filtrato['Submitted On'], errors='coerce')
            df_thd_filtrato = df_thd_filtrato.sort_values("Submitted On", ascending=False)
            df_thd_risultato = df_thd_filtrato[["Request/Report Number","Submitted On","Request/Report Subtype","Dealer","Question","Symptom","Solution","Status Reason","Product Type"]]
        else:
            df_thd_risultato = pd.DataFrame(columns=["Request/Report Number","Submitted On","Request/Report Subtype","Dealer","Question","Symptom","Solution","Status Reason","Product Type"])

        # Claim
        df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
        if not df_claim_filtrato.empty:
            df_claim_filtrato['Claim Payment Date'] = pd.to_datetime(df_claim_filtrato['Claim Payment Date'], errors='coerce')
            df_claim_filtrato = df_claim_filtrato.sort_values("Claim Payment Date", ascending=False)
            df_claim_risultato = df_claim_filtrato[["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"]]
        else:
            df_claim_risultato = pd.DataFrame(columns=["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"])

        # --- Scrittura Excel in memoria ---
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_icss_risultato.to_excel(writer, sheet_name="Report", index=False, startrow=0)
            startrow = len(df_icss_risultato) + 2
            df_thd_risultato.to_excel(writer, sheet_name="Report", index=False, startrow=startrow)
            startrow += len(df_thd_risultato) + 2
            df_claim_risultato.to_excel(writer, sheet_name="Report", index=False, startrow=startrow)

            # Opzioni formattazione colonna
            workbook = writer.book
            worksheet = writer.sheets["Report"]
            # Larghezza automatica delle colonne
            for df in [df_icss_risultato, df_thd_risultato, df_claim_risultato]:
                for i, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max_len)

        output.seek(0)
        return output

    except Exception as e:
        raise RuntimeError(f"Error generating Excel: {e}")
