import os
import pandas as pd

def genera_excel(esn, base_dir="."):
    excel_file = os.path.join(base_dir, f"Report_{esn}.xlsx")
    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")

    # --- Service ---
    df_service = pd.read_excel(os.path.join(base_dir, "Data Base Service.xlsx"))
    df_service_filtrato = df_service[df_service["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_service_filtrato.empty:
        df_service_filtrato['WAT_ORIGINAL'] = pd.to_datetime(df_service_filtrato['WAT_ORIGINAL'], errors='coerce')
        df_service_filtrato = df_service_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
        df_service_filtrato[["DOSSIER ID","WAT_ORIGINAL","DEALER","Engine Serial Number","Pre-diagnosis","Repair Description"]].to_excel(writer, sheet_name="ICSS", index=False)

    # --- THD ---
    df_thd = pd.read_excel(os.path.join(base_dir, "THD FM.xlsx"))
    df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_thd_filtrato.empty:
        df_thd_filtrato['Submitted On'] = pd.to_datetime(df_thd_filtrato['Submitted On'], errors='coerce')
        df_thd_filtrato = df_thd_filtrato.sort_values("Submitted On", ascending=False)
        df_thd_filtrato[["Request/Report Number","Submitted On","Request/Report Subtype","Dealer","Question","Symptom","Solution","Status Reason","Product Type"]].to_excel(writer, sheet_name="THD", index=False)

    # --- Claim ---
    df_claim = pd.read_excel(os.path.join(base_dir, "Data Base Warranty.xlsx"))
    df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
    if not df_claim_filtrato.empty:
        df_claim_filtrato['Claim Payment Date'] = pd.to_datetime(df_claim_filtrato['Claim Payment Date'], errors='coerce')
        df_claim_filtrato = df_claim_filtrato.sort_values("Claim Payment Date", ascending=False)
        df_claim_filtrato[["FPT Engine Family","Claim Number","Payed Dealer Name","Failure Comment","Claim Payment Date","Approved Amount","Local Currency Code"]].to_excel(writer, sheet_name="Claim", index=False)

    writer.close()
    return excel_file
