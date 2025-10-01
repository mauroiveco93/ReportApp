import streamlit as st
from genera_report import genera_report
from genera_excel import genera_excel
import os

# Imposta cartella base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Logo in alto a sinistra
logo_path = os.path.join(BASE_DIR, "logo.jpg")
try:
    st.image(logo_path, width=150)
except Exception:
    pass

st.title("Engine Report")  # titolo nell'app, rimane visibile

# Input ESN
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    st.success(f"ESN entered: {esn}")  # Messaggio di conferma inserimento

    # Bottoni per PDF o Excel
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate PDF"):
            try:
                pdf_path = genera_report(esn, BASE_DIR)
                st.success(f"PDF generated: {pdf_path}")
                st.download_button("Download PDF", pdf_path)
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    with col2:
        if st.button("Generate Excel"):
            try:
                excel_path = genera_excel(esn, BASE_DIR)
                st.success(f"Excel generated: {excel_path}")
                st.download_button("Download Excel", excel_path)
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
