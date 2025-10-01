import os
import streamlit as st
from genera_report import genera_report
from genera_excel import genera_excel

# App layout
base_dir = os.path.dirname(__file__)

logo_path = os.path.join(base_dir, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=150)

st.title("Engine Report Generator")

esn = st.text_input("Enter Engine Serial Number (ESN):")

if st.button("Generate PDF Report"):
    if esn:
        try:
            with st.spinner("Generating PDF report..."):
                pdf_path = genera_report(esn, base_dir)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
    else:
        st.warning("Please enter an ESN.")

if st.button("Generate Excel Report"):
    if esn:
        try:
            with st.spinner("Generating Excel report..."):
                excel_path = genera_excel(esn, base_dir)
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="Download Excel",
                    data=f,
                    file_name=os.path.basename(excel_path),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Error generating Excel: {e}")
    else:
        st.warning("Please enter an ESN.")
