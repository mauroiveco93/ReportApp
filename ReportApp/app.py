import streamlit as st
import os
import time
from genera_report import genera_report, genera_excel

# Titolo app
st.title("Motore Report")

# Cartella base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Logo
logo_path = os.path.join(base_dir, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
else:
    st.write("Logo not found")

# Input ESN
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn.strip():
    st.write("Ready to generate report for ESN:", esn)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate PDF"):
            progress = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)  # simulazione avanzamento
                progress.progress(i)
            try:
                pdf_file = os.path.join(base_dir, f"Report_{esn}.pdf")
                genera_report(esn, base_dir)
                st.success(f"Report generated: Report_{esn}.pdf")
                with open(pdf_file, "rb") as f:
                    st.download_button("Download PDF", f, file_name=f"Report_{esn}.pdf")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    with col2:
        if st.button("Generate Excel"):
            progress = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)
                progress.progress(i)
            try:
                excel_file = os.path.join(base_dir, f"Report_{esn}.xlsx")
                genera_excel(esn, base_dir)
                st.success(f"Excel generated: Report_{esn}.xlsx")
                with open(excel_file, "rb") as f:
                    st.download_button("Download Excel", f, file_name=f"Report_{esn}.xlsx")
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
else:
    st.warning("Please enter an ESN")
