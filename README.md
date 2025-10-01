# ESN Report Generator

**Generatore di report per motori FPT basato su Engine Serial Number (ESN)**

Questo progetto permette di generare un report PDF integrando informazioni provenienti da tre database Excel:

- **Dossier ICSS**: Interventi effettuati dalla rete su motori in garanzia  
- **THD FM**: Ticket aperti dalle officine verso casa madre  
- **Data Base Warranty**: Claim pagate relative agli interventi

Il report include tabelle con dettagli e KPI, ordinate cronologicamente, e può essere scaricato in PDF.

---

## Funzionalità principali

- Input interattivo dell’**ESN** tramite Streamlit  
- Generazione automatica di un PDF con:
  - Logo aziendale a sinistra  
  - Titoli delle sezioni: **Dossier ICSS**, **THD**, **Claim**  
  - Numero di casi e somma degli importi approvati nelle claim  
  - Tabelle leggibili con intestazioni grigio chiaro e testo a capo corretto  
- Ordinamento cronologico dei dati:
  - ICSS → `WAT_ORIGINAL`
  - THD → `Submitted On`
  - C
