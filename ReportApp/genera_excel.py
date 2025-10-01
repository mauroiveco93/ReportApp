import pandas as pd

def genera_excel(esn):
    try:
        excel_file = f"Report_{esn}.xlsx"

        # --- ICSS ---
        df_icss = pd.read_excel("Data Base Service.xlsx")
        df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
        df_icss_risultato = df_icss_filtrato[["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"]] if not df_icss_filtrato.empty else pd.DataFrame()

        # --- THD ---
        df_thd = pd.read_excel("THD FM.xlsx")
        df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
        df_thd_risultato = df_thd_filtrato[["Request/Report Number","Submitted On","Request/Report Subtype","Dealer","Question","Symptom","Solution","Status Reason","Product Type"]] if not df_thd_filtrato.empty else pd.DataFrame()

        # --- Claim ---
        df_claim = pd.read_excel("Data Base Warranty.xlsx")
        df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
        df_claim_risultato = df_claim_filtrato[["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"]] if not df_claim_filtrato.empty else pd.DataFrame()

        # Scrivi tutto in un singolo file Excel con righe vuote tra i dataframe
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df_icss_risultato.to_excel(writer, sheet_name='Report', index=False)
            startrow = len(df_icss_risultato) + 2
            df_thd_risultato.to_excel(writer, sheet_name='Report', index=False, startrow=startrow)
            startrow += len(df_thd_risultato) + 2
            df_claim_risultato.to_excel(writer, sheet_name='Report', index=False, startrow=startrow)

        return excel_file
    except Exception as e:
        raise RuntimeError(f"Error generating Excel: {e}")
