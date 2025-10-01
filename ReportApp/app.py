import streamlit as st
from generate import genera_report, genera_excel
from io import BytesIO
import time

st.set_page_config(page_title="Report Engine", layout="wide")

# Logo in alto
st.image("logo.jpg", width=150)

st.title("Report Engine")

# Inserimento ESN
esn = st.text_input("Insert Engine Serial Number (ESN)")

if esn:
    st.write(f"Generating report for ESN: {esn} ...")

    # Barra di progresso fittizia
    progress_bar = st.progress(0)
    for i in range(101):
        time.sleep(0.01)
        progress_bar.progress(i)

    # Genera PDF
    try:
        pdf_buffer = genera_report(esn)
        st.success("✅ PDF generated successfully")
        st.download_button(label="Download PDF", data=pdf_buffer, file_name=f"Report_{esn}.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"Error generating PDF: {e}")

    # Genera Excel
    try:
        excel_buffer = genera_excel(esn)
        st.success("✅ Excel generated successfully")
        st.download_button(label="Download Excel", data=excel_buffer, file_name=f"Report_{esn}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error generating Excel: {e}")
