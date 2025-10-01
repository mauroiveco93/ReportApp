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

st.title("Engine Report")

# Input ESN
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    st.success(f"You entered ESN: {esn}")

    # --- PDF Section ---
    if st.button("Create PDF"):
        progress_text = "Generating PDF..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)  # finta progressione
            my_bar.progress(percent_complete + 1, text=progress_text)
        try:
            pdf_file = genera_report(esn, base_dir)
            st.success("PDF generated successfully!")
        except Exception as e:
            st.error(f"Error generating PDF: {e}")

    if 'pdf_file' in locals():
        st.download_button(
            label="Download PDF",
            data=open(pdf_file, "rb").read(),
            file_name=os.path.basename(pdf_file),
            mime="application/pdf"
        )

    # --- Excel Section ---
    if st.button("Create Excel"):
        progress_text = "Generating Excel..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)  # finta progressione
            my_bar.progress(percent_complete + 1, text=progress_text)
        try:
            excel_file = genera_excel(esn, base_dir)
            st.success("Excel generated successfully!")
        except Exception as e:
            st.error(f"Error generating Excel: {e}")

    if 'excel_file' in locals():
        st.download_button(
            label="Download Excel",
            data=open(excel_file, "rb").read(),
            file_name=os.path.basename(excel_file),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
