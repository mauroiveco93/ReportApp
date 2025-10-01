import streamlit as st
import os
from genera_report import genera_report, genera_excel
import time

st.set_page_config(page_title="Engine Report", layout="wide")

# === Percorsi file ===
logo_path = "logo.jpg"

# === Intestazione Logo + Titolo ===
col1, col2 = st.columns([1,4])
with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
with col2:
    st.markdown("## Engine Report")

st.write("---")

# === Input ESN ===
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    st.write(f"Generating report for ESN: **{esn}**")
    
    # === Barra di avanzamento reale ===
    steps = ["Loading ICSS", "Loading THD", "Loading Claim", "Generating PDF", "Generating Excel"]
    progress = st.progress(0)
    
    status_text = st.empty()
    
    # --- Step 1: ICSS ---
    status_text.text("Step 1/5: Loading ICSS...")
    time.sleep(0.5)  # simulazione o puoi sostituire con funzione reale
    progress.progress(20)
    
    # --- Step 2: THD ---
    status_text.text("Step 2/5: Loading THD...")
    time.sleep(0.5)
    progress.progress(40)
    
    # --- Step 3: Claim ---
    status_text.text("Step 3/5: Loading Claim...")
    time.sleep(0.5)
    progress.progress(60)
    
    # --- Step 4: Genera PDF ---
    status_text.text("Step 4/5: Generating PDF...")
    try:
        pdf_file = genera_report(esn)
        progress.progress(80)
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        progress.progress(0)
    
    # --- Step 5: Genera Excel ---
    status_text.text("Step 5/5: Generating Excel...")
    try:
        excel_file = genera_excel(esn)
        progress.progress(100)
    except Exception as e:
        st.error(f"Error generating Excel: {e}")
    
    status_text.text("Done!")
    st.success("Report generated successfully!")

    st.write("---")
    
    # === Pulsanti di download ===
    col_pdf, col_excel = st.columns(2)
    
    with col_pdf:
        if pdf_file and os.path.exists(pdf_file):
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_file),
                    mime="application/pdf"
                )
    
    with col_excel:
        if excel_file and os.path.exists(excel_file):
            with open(excel_file, "rb") as f:
                st.download_button(
                    label="Download Excel",
                    data=f,
                    file_name=os.path.basename(excel_file),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
