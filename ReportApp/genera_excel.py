import pandas as pd
import os

def genera_excel(esn, base_dir):
    excel_file = os.path.join(base_dir, f"Report_{esn}.xlsx")

    # --- Logica per generare i dataframe df_icss_risultato, df_thd_risultato, df_claim_risultato ---
    # Concatenare i dati in un unico file con riga vuota tra tabelle

    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        # df_icss_risultato.to_excel(writer, sheet_name='Report', index=False)
        # Aggiungi riga vuota
        # df_thd_risultato.to_excel(writer, sheet_name='Report', startrow=len(df_icss_risultato)+2, index=False)
        # df_claim_risultato.to_excel(writer, sheet_name='Report', startrow=len(df_icss_risultato)+len(df_thd_risultato)+4, index=False)
        pass

    return excel_file
