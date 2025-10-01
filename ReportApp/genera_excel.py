import pandas as pd
import os

def genera_excel(esn, base_dir="."):
    try:
        excel_file = os.path.join(base_dir, f"Report_{esn}.xlsx")
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

        # --- Dossier ICSS ---
        df_icss = pd.read_excel(os.path.join(base_dir, "data", "Data Base Service.xlsx"))
        df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)]
        if not df_icss_filtrato.empty:
            df_icss_filtrato.to_excel(writer, sheet_name="Report", index=False, startrow=0)
            startrow = len(df_icss_filtrato) + 2
        else:
            startrow = 0

        # --- THD ---
        df_thd = pd.read_excel(os.path.join(base_dir, "data", "THD FM.xlsx"))
        df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)]
        if not df_thd_filtrato.empty:
            df_thd_filtrato.to_excel(writer, sheet_name="Report", index=False, startrow=startrow)
            startrow += len(df_thd_filtrato) + 2

        # --- Claim ---
        df_claim = pd.read_excel(os.path.join(base_dir, "data", "Data Base Warranty.xlsx"))
        df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)]
        if not df_claim_filtrato.empty:
            df_claim_filtrato.to_excel(writer, sheet_name="Report", index=False, startrow=startrow)

        writer.save()
        return excel_file
    except Exception as e:
        raise RuntimeError(f"Error generating Excel: {e}")
