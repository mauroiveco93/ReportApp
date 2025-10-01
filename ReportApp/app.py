import streamlit as st
import os
from genera_report import genera_report
from genera_excel import genera_excel
import time

# === BASE DIRECTORY ===
base_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Engine Report", layout="wide")

# Logo in alto a sinistra
logo_path = os.path.join(base_dir, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=150)

st.title("Engine Report")  # solo visivo, sotto ci sarà Report for ESN

# Input ESN
esn = st.text_input("Enter Engine Serial Number (ESN):")
if esn:
    st.success(f"ESN entered: {esn}")

    # Barra di avanzamento simulata
    progress_text = "Generating report..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)  # simulazione di avanzamento
        my_bar.progress(percent_complete + 1, text=progress_text)

    st.write("Select the report format:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Download PDF"):
            try:
                pdf_file = genera_report(esn, base_dir)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=os.path.basename(pdf_file),
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    with col2:
        if st.button("Download Excel"):
            try:
                excel_file = genera_excel(esn, base_dir)
                with open(excel_file, "rb") as f:
                    st.download_button(
                        label="Download Excel",
                        data=f,
                        file_name=os.path.basename(excel_file),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
