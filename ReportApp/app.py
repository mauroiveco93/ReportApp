import streamlit as st
from generate import genera_report, genera_excel
import os

st.set_page_config(page_title="Report App", layout="wide")

current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "logo.jpg")

# Logo
try:
    st.image(logo_path, width=150)
except:
    st.title("Report App")

st.title("Engine Serial Number Report")

# Inserimento ESN
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    progress_bar = st.progress(0)
    st.write("Generating report...")

    # PDF
    pdf_file = genera_report(esn)
    progress_bar.progress(50)

    # Excel
    excel_file = genera_excel(esn)
    progress_bar.progress(100)

    # Download buttons
    st.download_button("Download PDF", pdf_file, file_name=f"Report_{esn}.pdf", mime="application/pdf")
    st.download_button("Download Excel", excel_file, file_name=f"Report_{esn}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
