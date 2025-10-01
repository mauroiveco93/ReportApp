import pandas as pd
import os

def genera_excel(esn, base_dir="."):
    """
    Genera un file Excel con i dati filtrati dai tre database
    in base all'ESN fornito.
    """
    try:
        excel_file = os.path.join(base_dir, f"Report_{esn}.xlsx")
        writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")

        # --- Dossier ICSS ---
        df_icss = pd.read_excel(os.path.join(base_dir, "Data Base Service.xlsx"))
        df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
        if not df_icss_filtrato.empty:
            df_icss_filtrato['WAT_ORIGINAL'] = pd.to_datetime(df_icss_filtrato['WAT_ORIGINAL'], errors='coerce')
            df_icss_filtrato = df_icss_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
            df_icss_risultato = df_icss_filtrato[["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"]]
        else:
            df_icss_risultato = pd.DataFrame()
        df_icss_risultato.to_excel(writer, sheet_name="Report", startrow=0, index=False)

        # --- THD ---
        df_thd = pd.read_excel(os.path.join(base_dir, "THD FM.xlsx"))
        df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
        if not df_thd_filtrato.empty:
            df_thd_filtrato['Submitted On'] = pd.to_datetime(df_thd_filtrato['Submitted On'], errors='coerce')
            df_thd_filtrato = df_thd_filtrato.sort_values("Submitted On", ascending=False)
            df_thd_risultato = df_thd_filtrato[["Request/Report Number","Submitted On","Request/Report Subtype","Dealer","Question","Symptom","Solution","Status Reason","Product Type"]]
        else:
            df_thd_risultato = pd.DataFrame()
        startrow = len(df_icss_risultato) + 2 if not df_icss_risultato.empty else 0
        df_thd_risultato.to_excel(writer, sheet_name="Report", startrow=startrow, index=False)

        # --- Claim ---
        df_claim = pd.read_excel(os.path.join(base_dir, "Data Base Warranty.xlsx"))
        df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
        if not df_claim_filtrato.empty:
            df_claim_filtrato['Claim Payment Date'] = pd.to_datetime(df_claim_filtrato['Claim Payment Date'], errors='coerce')
            df_claim_filtrato = df_claim_filtrato.sort_values("Claim Payment Date", ascending=False)
            df_claim_risultato = df_claim_filtrato[["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"]]
        else:
            df_claim_risultato = pd.DataFrame()
        startrow = startrow + len(df_thd_risultato) + 2 if not df_thd_risultato.empty else startrow
        df_claim_risultato.to_excel(writer, sheet_name="Report", startrow=startrow, index=False)

        writer.save()
        return excel_file

    except Exception as e:
        raise RuntimeError(f"Error generating Excel: {e}")
