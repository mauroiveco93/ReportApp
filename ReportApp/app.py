import streamlit as st
from genera_report import genera_report
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "logo.jpg")

# Mostra logo in Streamlit
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=150)

st.title("Engine Serial Number Report")

esn = st.text_input("Enter Engine Serial Number (ESN)")

if st.button("Generate Report") and esn:
    try:
        pdf_file = genera_report(esn)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name=f"Report_{esn}.pdf",
                mime="application/pdf"
            )
        st.success("✅ Report generated successfully!")
    except Exception as e:
        st.error(f"❌ Error generating report: {e}")
