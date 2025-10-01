import streamlit as st
import os
from genera_report import genera_report
from genera_excel import genera_excel

st.set_page_config(page_title="Engine Report", layout="centered")

# Logo
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=150)

st.title("Engine Report")

esn = st.text_input("Inserisci Engine Serial Number (ESN)")

if esn:
    if st.button("📄 Scarica PDF"):
        with st.spinner("Generazione PDF in corso..."):
            try:
                pdf_path = genera_report(esn, base_dir=".")
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name=os.path.basename(pdf_path))
            except Exception as e:
                st.error(f"Errore generazione PDF: {e}")

    if st.button("📊 Scarica Excel"):
        with st.spinner("Generazione Excel in corso..."):
            try:
                excel_path = genera_excel(esn, base_dir=".")
                with open(excel_path, "rb") as f:
                    st.download_button("Download Excel", f, file_name=os.path.basename(excel_path))
            except Exception as e:
                st.error(f"Errore generazione Excel: {e}")
