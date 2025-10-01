import streamlit as st
from genera_report import genera_report
import os

st.set_page_config(page_title="Generatore Report Motore", layout="wide")
st.image("logo.jpg", width=150)
st.title("Generatore Report Motore")

esn = st.text_input("Inserisci Engine Serial Number (ESN)")

if st.button("Genera Report"):
    if esn.strip() == "":
        st.warning("Inserisci un ESN valido!")
    else:
        try:
            genera_report(esn)
            pdf_path = f"Report_{esn}.pdf"
            if os.path.exists(pdf_path):
                st.success(f"Report generato: {pdf_path}")
                with open(pdf_path, "rb") as f:
                    st.download_button("Scarica PDF", f, file_name=pdf_path)
        except Exception as e:
            st.error(f"Errore durante la generazione del report: {e}")