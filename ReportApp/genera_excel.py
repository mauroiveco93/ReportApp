import os
import pandas as pd

def genera_excel(esn, base_dir):
    excel_file = f"Report_{esn}.xlsx"
    try:
        # Percorsi dei file
        service_path = os.path.join(base_dir, "data", "Data Base Service.xlsx")
        thd_path = os.path.join(base_dir, "data", "THD FM.xlsx")
        claim_path = os.path.join(base_dir, "data", "Data Base Warranty.xlsx")

        # --- ICSS ---
        df_icss = pd.read_excel(service_path)
        df_icss_filtrato = df_icss[df_icss["Engine Serial Number"].astype(str) == str(esn)].copy()
        if not df_icss_filtrato.empty:
            df_icss_filtrato['WAT_ORIGINAL'] = pd.to_datetime(df_icss_filtrato['WAT_ORIGINAL'], errors='coerce')
            df_icss_filtrato = df_icss_filtrato.sort_values("WAT_ORIGINAL", ascending=False)
            df_icss_result = df_icss_filtrato[
    ["DOSSIER ID", "WAT_ORIGINAL", "DEALER", "Engine Serial Number", "Pre-diagnosis", "Repair Description"]
]
        else:
            df_icss_result = pd.DataFrame(columns=["DOSSIER ID", "WAT_ORIGINAL", "DEALER", "Engine Serial Number", "Pre-diagnosis", "Repair Description"])

        # --- THD ---
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

        # --- Claims ---
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

        # Scrive in un file Excel con tre fogli separati
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df_icss_result.to_excel(writer, sheet_name="ICSS", index=False)
            df_thd_result.to_excel(writer, sheet_name="THD", index=False)
            df_claim_result.to_excel(writer, sheet_name="Claims", index=False)

        return excel_file

    except Exception as e:
        raise Exception(f"Error generating Excel: {e}")
