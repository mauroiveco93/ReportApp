import os
import pandas as pd


def genera_excel(esn, base_dir):
    excel_file = f"Report_{esn}.xlsx"
    excel_path = os.path.join(base_dir, excel_file)

    writer = pd.ExcelWriter(excel_path, engine="xlsxwriter")

    # --- ICSS ---
    df_icss = pd.read_excel(os.path.join(base_dir, "data", "Data Base Service.xlsx"))
    df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_icss_filtrato.empty:
        df_icss_result = df_icss_filtrato[
            ["DOSSIER ID", "WAT_ORIGINAL", "DEALER", "Engine Serial Number", "Pre-diagnosis", "Repair Description"]
        ]
    else:
        df_icss_result = pd.DataFrame()
    df_icss_result.to_excel(writer, sheet_name="ICSS", index=False)

    # --- THD ---
    df_thd = pd.read_excel(os.path.join(base_dir, "data", "THD FM.xlsx"))
    df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_thd_filtrato.empty:
        df_thd_result = df_thd_filtrato[
            ["Request/Report Number", "Submitted On", "Request/Report Subtype", "Dealer",
             "Question", "Symptom", "Solution", "Status Reason", "Product Type"]
        ]
    else:
        df_thd_result = pd.DataFrame()
    df_thd_result.to_excel(writer, sheet_name="THD", index=False)

    # --- Claims ---
    df_claim = pd.read_excel(os.path.join(base_dir, "data", "Data Base Warranty.xlsx"))
    df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
    if not df_claim_filtrato.empty:
        df_claim_result = df_claim_filtrato[
            ["FPT Engine Family", "Claim Number", "Payed Dealer Name",
             "Failure Comment", "Claim Payment Date", "Approved Amount", "Local Currency Code"]
        ]
    else:
        df_claim_result = pd.DataFrame()
    df_claim_result.to_excel(writer, sheet_name="Claims", index=False)

    writer.close()
    return excel_path
