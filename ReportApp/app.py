import streamlit as st
from genera_report import genera_report
from genera_excel import genera_excel
import time
import os

st.set_page_config(page_title="Engine Report", layout="wide")

# --- Logo and title ---
col1, col2 = st.columns([1, 6])
with col1:
    try:
        st.image("logo.jpg", width=120)
    except:
        st.write("Logo not found")
with col2:
    st.title("Engine Report")

st.write("---")

# --- User input ---
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    # --- Progress bar ---
    progress_text = st.empty()
    progress_bar = st.progress(0)

    def update_progress():
        for i in range(1, 101):
            progress_text.text(f"Processing... {i}%")
            progress_bar.progress(i)
            time.sleep(0.01)  # simulate realistic processing

    update_progress()

    st.write("Choose output format:")
    col_pdf, col_excel = st.columns(2)

    with col_pdf:
        if st.button("Generate PDF"):
            try:
                pdf_file = genera_report(esn)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    with col_excel:
        if st.button("Generate Excel"):
            try:
                excel_file = genera_excel(esn)
                with open(excel_file, "rb") as f:
                    st.download_button(
                        label="Download Excel",
                        data=f,
                        file_name=excel_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
