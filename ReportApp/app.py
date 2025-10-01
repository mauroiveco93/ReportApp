import streamlit as st
from genera_report import genera_report
from genera_excel import genera_excel
import os
import time

st.set_page_config(page_title="Engine Report", layout="wide")

# Logo + title
logo_path = os.path.join("logo.jpg")
if os.path.exists(logo_path):
    col1, col2 = st.columns([1,5])
    with col1:
        st.image(logo_path, width=150)
    with col2:
        st.title("Engine Report")
else:
    st.title("Engine Report")

# ESN input
esn = st.text_input("Enter Engine Serial Number:")

if esn:
    # barra di progresso simulata
    progress_text = "Generating report..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(101):
        time.sleep(0.01)  # simulazione lavoro
        my_bar.progress(percent_complete, text=progress_text)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Download PDF"):
            try:
                pdf_file = genera_report(esn, base_dir=".")
                with open(pdf_file, "rb") as f:
                    st.download_button("Click to download PDF", f, file_name=os.path.basename(pdf_file))
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    with col2:
        if st.button("Download Excel"):
            try:
                excel_file = genera_excel(esn, base_dir=".")
                with open(excel_file, "rb") as f:
                    st.download_button("Click to download Excel", f, file_name=os.path.basename(excel_file))
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
