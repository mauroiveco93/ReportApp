import streamlit as st
from generate import genera_report

st.title("Engine Report Generator")

# Inserisci ESN
esn = st.text_input("Enter Engine Serial Number (ESN)")

# Bottone genera report
if st.button("Generate PDF") and esn:
    try:
        pdf_buffer = genera_report(esn)
        st.success("Report generated successfully!")
        st.download_button(
            "Download PDF",
            data=pdf_buffer,
            file_name=f"Report_{esn}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Errore nella generazione del report: {e}")
