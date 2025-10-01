import streamlit as st
from generate import genera_report, genera_excel

st.set_page_config(page_title="Report App", layout="wide")
st.title("Report Generator")

# Logo a sinistra
st.image("logo.jpg", width=150)

# Input ESN
esn = st.text_input("Enter Engine Serial Number (ESN):")

if esn:
    st.info("Generating report...")

    # Progress bar
    import time
    progress = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        progress.progress(i)

    # PDF
    pdf_data = genera_report(esn)
    st.download_button(
        label="Download PDF",
        data=pdf_data,
        file_name=f"Report_{esn}.pdf",
        mime="application/pdf"
    )

    # Excel
    excel_data = genera_excel(esn)
    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name=f"Report_{esn}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
