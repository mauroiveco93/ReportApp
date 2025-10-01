import streamlit as st
from genera_report import genera_report

st.set_page_config(page_title="Engine Report", layout="wide")

st.title("Engine Report Generator")

# Inserimento ESN
esn = st.text_input("Insert Engine Serial Number (ESN):")

if st.button("Generate Report") and esn:
    try:
        pdf_file = genera_report(esn)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download Report PDF",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"❌ Error generating report: {e}")
