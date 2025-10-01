import streamlit as st
import os
from genera_report import genera_report, genera_excel
import time

# --- Imposta cartella base ---
base_dir = os.path.dirname(__file__)

# --- Logo e titolo ---
logo_path = os.path.join(base_dir, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
st.title("Engine Report")
st.write("---")

# --- Input ESN ---
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    # Barra di avanzamento
    progress_text = "Processing..."
    my_bar = st.progress(0, text=progress_text)

    # Simula caricamento per i tre database
    for i, step in enumerate(["Reading Dossier ICSS...", "Reading THD...", "Reading Claims..."], start=1):
        my_bar.progress(int(i*33.3), text=step)
        time.sleep(0.5)  # simulazione caricamento

    # Completa 100%
    my_bar.progress(100, text="Generating report...")

    # --- Generazione PDF ---
    try:
        pdf_file = genera_report(esn, base_dir)
        st.success("PDF generated successfully!")
        st.download_button(
            label="Download PDF",
            data=open(pdf_file, "rb").read(),
            file_name=os.path.basename(pdf_file),
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error generating PDF: {e}")

    # --- Generazione Excel ---
    try:
        excel_file = genera_excel(esn, base_dir)
        st.success("Excel generated successfully!")
        st.download_button(
            label="Download Excel",
            data=open(excel_file, "rb").read(),
            file_name=os.path.basename(excel_file),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error generating Excel: {e}")
