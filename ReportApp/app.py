import streamlit as st
import os
from genera_report import genera_report  # la tua funzione che crea il PDF

# ======== Layout della pagina ========
st.set_page_config(
    page_title="Report Generator",
    layout="wide"
)

# ======== Logo a sinistra ========
logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=150, use_container_width=False)

# ======== Titolo ========
st.title("ESN Report Generator")

st.markdown("""
Inserisci il **Engine Serial Number (ESN)** per generare il report dai database.
""")

# ======== Input interattivo ========
esn = st.text_input("Engine Serial Number")

# ======== Bottone per generare il report ========
if st.button("Genera Report"):
    if esn.strip() == "":
        st.warning("⚠️ Inserisci un ESN valido!")
    else:
        try:
            pdf_file = genera_report(esn.strip())  # la funzione che hai già creato
            st.success(f"✅ Report generato: {pdf_file}")
            # Mostra link per scaricare il PDF
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Scarica PDF",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ Errore nella generazione del report: {e}")
