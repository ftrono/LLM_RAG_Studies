import streamlit as st
import pandas as pd
import modulo_1a
import modulo_1b

# Funzione principale
def main():
    st.set_page_config()
    st.sidebar.title('Navigazione')
    # Tasti per la navigazione tra le pagine
    page = st.sidebar.radio("Seleziona il modulo", ['Modulo 1a: Ricerca semantica per dati identificativi', 'Modulo 1b'])
    if page == 'Modulo 1a: Ricerca semantica per dati identificativi':
        modulo_1a.page_one()
    elif page == '''Modulo 1b: Ricerca semantica per testo inserito dall'utente''':
        modulo_1b.page_two()
        
if __name__ == '__main__':
    main()



