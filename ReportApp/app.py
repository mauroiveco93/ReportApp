import os
import streamlit as st
from genera_report import genera_report
from genera_excel import genera_excel

# Percorso base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Logo e titolo
logo_path = os.path.join(BASE_DIR, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=120)
st.title("Engine Report")

# Input ESN
esn = st.text_input("Inserisci ESN:")

# Barra di avanzamento
progress_bar = st.progress(0)
status_text = st.empty()

if esn:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Genera PDF"):
            try:
                progress_bar.progress(20)
                status_text.text("Caricamento dati...")

                output_path = os.path.join(BASE_DIR, f"Report_{esn}.pdf")
                genera_report(esn, output_path, BASE_DIR)

                progress_bar.progress(100)
                status_text.text("Completato!")

                with open(output_path, "rb") as file:
                    st.download_button(
                        "Scarica PDF",
                        file,
                        file_name=f"Report_{esn}.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Errore generazione PDF: {e}")

    with col2:
        if st.button("Genera Excel"):
            try:
                progress_bar.progress(20)
                status_text.text("Caricamento dati...")

                output_path = os.path.join(BASE_DIR, f"Report_{esn}.xlsx")
                genera_excel(esn, output_path, BASE_DIR)

                progress_bar.progress(100)
                status_text.text("Completato!")

                with open(output_path, "rb") as file:
                    st.download_button(
                        "Scarica Excel",
                        file,
                        file_name=f"Report_{esn}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Errore generazione Excel: {e}")
