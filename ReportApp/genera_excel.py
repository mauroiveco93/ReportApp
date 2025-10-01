import os
import pandas as pd

def genera_excel(esn, output_path, base_dir):
    try:
        # Percorsi file
        service_file = os.path.join(base_dir, "data", "Data Base Service.xlsx")
        thd_file = os.path.join(base_dir, "data", "THD FM.xlsx")
        warranty_file = os.path.join(base_dir, "data", "Data Base Warranty.xlsx")

        # Carica i dati
        df_service = pd.read_excel(service_file)
        df_thd = pd.read_excel(thd_file)
        df_warranty = pd.read_excel(warranty_file)

        # Filtra
        service_data = df_service[df_service['ESN'] == esn]
        thd_data = df_thd[df_thd['ESN'] == esn]
        warranty_data = df_warranty[df_warranty['ESN'] == esn]

        # Scrive Excel
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            if not service_data.empty:
                service_data.to_excel(writer, sheet_name="Service", index=False)
            if not thd_data.empty:
                thd_data.to_excel(writer, sheet_name="THD", index=False)
            if not warranty_data.empty:
                warranty_data.to_excel(writer, sheet_name="Warranty", index=False)

        return output_path
    except Exception as e:
        raise RuntimeError(f"Errore nella generazione dell'Excel: {e}")
