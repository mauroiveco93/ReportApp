import streamlit as st
import os
from genera_report import genera_report
from genera_excel import genera_excel  # Assicurati di avere questo file nello stesso repo
import time

st.set_page_config(page_title="Engine Report", layout="wide")

# --- Header logo ---
logo_path = "logo.jpg"
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
st.title("Engine Report")

st.write("Enter the Engine Serial Number (ESN) below:")

# --- Input ESN ---
esn = st.text_input("ESN", "")
if esn:
    st.success(f"ESN entered: {esn}")

    # --- Barra di avanzamento ---
    progress_text = "Generating report..."
    progress_bar = st.progress(0, text=progress_text)

    # Simulazione progressiva
    for percent_complete in range(0, 101, 10):
        time.sleep(0.1)  # piccolo delay per simulare lavoro
        progress_bar.progress(percent_complete, text=progress_text)

    st.write("Choose report format to download:")

    # --- Bottoni PDF / Excel ---
    col1, col2 = st.columns(2)

    base_dir = os.getcwd()  # cartella corrente del repo

    with col1:
        if st.button("Download PDF"):
            try:
                pdf_file = genera_report(esn, base_dir)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )
            excep
