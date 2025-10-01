import streamlit as st
import os
from genera_report import genera_report

st.set_page_config(page_title="Report Generator", layout="wide")

# Logo a sinistra
BASE_DIR = os.path.dirname(__file__)
logo_path = os.path.join(BASE_DIR, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=150, use_container_width=False)

st.title("ESN Report Generator")
st.markdown("Inserisci il **Engine Serial Number (ESN)** per generare il report dai database.")

# Input interattivo ESN
esn = st.text_input("Engine Serial Number")

# Bottone genera report
if st.button("Genera Report"):
    if esn.strip() == "":
        st.warning("⚠️ Inserisci un ESN valido!")
    else:
        try:
            pdf_file = genera_report(esn.strip())
            st.success(f"✅ Report generato: {os.path.basename(pdf_file)}")
            # Download PDF
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Scarica PDF",
                    data=f,
                    file_name=os.path.basename(pdf_file),
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ Errore nella generazione del report: {e}")
