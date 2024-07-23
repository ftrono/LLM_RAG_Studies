import streamlit as st
import pandas as pd
from globals import * 

# Funzione per la prima pagina
def page_one():
    with st.form(key='form'):
        st.title('Modulo 1a')
        
        
        oggetto = st.text_area("Oggetto", height=100)
        
        # Creazione delle celle di testo
        cols = st.columns(4)  # 4 colonne per riga
        
        # Prima riga di celle
        with cols[0]:
            aoo = st.text_input("AOO (Area Organizzativa Omogenea)")
        with cols[1]:
            tipoAtto = st.text_input("Tipo Atto")
        with cols[2]:
            tipoDeterminazione = st.text_input("Tipo Determinazione")

        # Seconda riga di celle
        cols = st.columns(4)  # 4 colonne per riga
        with cols[0]:
            tipoIterBurocratico = st.text_input("Tipo Iter Burocratico")
        with cols[1]:
            tipoMateria = st.text_input("Tipo Materia")
        with cols[2]:
            materia = st.text_input("Materia")
        with cols[3]:
            sottoMateria = st.text_input("Sotto Materia")
        
        #Bottone di submit
        submit_button = st.form_submit_button(label='Ricerca documento')
        
        if submit_button:
            query_oggetto=f"Oggetto: {oggetto}"
            query_aoo=f"Area Organizzativa Omogenea: {aoo}"
            query_tipoAtto=f"Tipo Atto: {tipoAtto}"
            query_tipoDeterminazione=f"Tipo Determinazione: {tipoDeterminazione}"
            query_tipoIterBurocratico=f"Tipo Iter Burocratico: {tipoIterBurocratico}"
            query_tipoMateria=f"Tipo Materia: {tipoMateria}"
            query_materia=f"Materia: {materia}"
            query_sottoMateria=f"Sotto Materia: {sottoMateria}"
            
            query="\n".join([query_oggetto,query_aoo,query_tipoAtto,query_tipoDeterminazione,
                            query_tipoIterBurocratico,query_tipoMateria,query_materia,query_sottoMateria])
            
            #Effettuo la query al DB
            #Found_documents=llm.invoke(query)
            SourcesList=["1", "2", "3"]   #retrieve with RAG
        
            st.text(SourcesList[0])
            st.text(SourcesList[1])
            st.text(SourcesList[2])
