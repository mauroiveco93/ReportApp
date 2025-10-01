import os
import pandas as pd

def genera_excel(esn, base_dir):
    excel_file = f"Report_{esn}.xlsx"
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    # --- ICSS ---
    service_path = os.path.join(base_dir, "data", "Data Base Service.xlsx")
    df_icss = pd.read_excel(service_path)
    df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_icss_filtrato.empty:
        df_icss_filtrato['WAT_ORIGINAL'] = pd.to_datetime(df_icss_filtrato['WAT_ORIGINAL'], errors='coerce')
        df_icss_filtrato = df_icss_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
        df_icss_result = df_icss_filtrato[
            ["DOSSIER ID", "WAT_ORIGINAL", "DEALER", "Engine Serial Number", "Pre-diagnosis", "Repair Description"]
        ]
    else:
        df_icss_result = pd.DataFrame(columns=["DOSSIER ID", "WAT_ORIGINAL", "DEALER", "Engine Serial Number",
                                               "Pre-diagnosis", "Repair Description"])
    startrow = 0
    df_icss_result.to_excel(writer, sheet_name="Report", startrow=startrow, index=False)
    startrow += len(df_icss_result) + 2  # aggiunge riga vuota

    # --- THD ---
    thd_path = os.path.join(base_dir, "data", "THD FM.xlsx")
    df_thd = pd.read_excel(thd_path)
    df_thd_filtrato = df_thd[df_thd["Engine Serial Number"].astype(str) == str(esn)].copy()
    if not df_thd_filtrato.empty:
        df_thd_filtrato['Submitted On'] = pd.to_datetime(df_thd_filtrato['Submitted On'], errors='coerce')
        df_thd_filtrato = df_thd_filtrato.sort_values("Submitted On", ascending=False)
        df_thd_result = df_thd_filtrato[
            ["Request/Report Number", "Submitted On", "Request/Report Subtype", "Dealer",
             "Question", "Symptom", "Solution", "Status Reason", "Product Type"]
        ]
    else:
        df_thd_result = pd.DataFrame(columns=[
            "Request/Report Number", "Submitted On", "Request/Report Subtype", "Dealer",
            "Question", "Symptom", "Solution", "Status Reason", "Product Type"
        ])
    df_thd_result.to_excel(writer, sheet_name="Report", startrow=startrow, index=False)
    startrow += len(df_thd_result) + 2

    # --- Claims ---
    claim_path = os.path.join(base_dir, "data", "Data Base Warranty.xlsx")
    df_claim = pd.read_excel(claim_path)
    df_claim_filtrato = df_claim[df_claim["FPT Serial Number Customer"].astype(str) == str(esn)].copy()
    if not df_claim_filtrato.empty:
        df_claim_filtrato['Claim Payment Date'] = pd.to_datetime(df_claim_filtrato['Claim Payment Date'], errors='coerce')
        df_claim_filtrato = df_claim_filtrato.sort_values("Claim Payment Date", ascending=False)
        df_claim_result = df_claim_filtrato[
            ["FPT Engine Family", "Claim Number", "Payed Dealer Name",
             "Failure Comment", "Claim Payment Date", "Approved Amount", "Local Currency Code"]
        ]
    else:
        df_claim_result = pd.DataFrame(columns=[
            "FPT Engine Family", "Claim Number", "Payed Dealer Name",
            "Failure Comment", "Claim Payment Date", "Approved Amount", "Local Currency Code"
        ])
    df_claim_result.to_excel(writer, sheet_name="Report", startrow=startrow, index=False)

    writer.save()
    return excel_file
