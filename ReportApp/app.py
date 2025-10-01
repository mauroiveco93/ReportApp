import streamlit as st
import os
from genera_report import genera_report
from genera_excel import genera_excel
import time

# Cartella base (dove risiedono app.py, logo e database)
BASE_DIR = "."

# Logo in alto a sinistra
logo_path = os.path.join(BASE_DIR, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=150)
st.markdown("## Engine Report")
st.write("---")

# Input ESN
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    st.write(f"Generating report for ESN: **{esn}**")
    
    # Barra di avanzamento simulata
    progress_text = "Progressing..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(0, 101, 10):
        my_bar.progress(percent_complete, text=progress_text)
        time.sleep(0.05)  # Simula tempo di elaborazione
    my_bar.empty()
    
    col1, col2 = st.columns(2)
    
    # Bottone PDF
    with col1:
        if st.button("Download PDF"):
            try:
                pdf_file = genera_report(esn, base_dir=BASE_DIR)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=os.path.basename(pdf_file),
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
    
    # Bottone Excel
    with col2:
        if st.button("Download Excel"):
            try:
                excel_file = genera_excel(esn, base_dir=BASE_DIR)
                with open(excel_file, "rb") as f:
                    st.download_button(
                        label="Download Excel",
                        data=f,
                        file_name=os.path.basename(excel_file),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
