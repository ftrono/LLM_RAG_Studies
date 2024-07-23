import streamlit as st
import pandas as pd
from globals import * 

# Funzione per la prima pagina
def page_two():
    with st.form(key='form'):
        st.title('Modulo 1a')
        query = st.text_area("Cosa vuoi cercare?", height=100)
        
        #Bottone di submit
        submit_button = st.form_submit_button(label='Ricerca documento')
        
        if submit_button:
            
            #Effettuo la query al DB
            #Found_documents=RETRIEVER.invoke(query)
            SourcesList=["1", "2", "3"]   #retrieve with RAG
        
            st.text(SourcesList[0])
            st.text(SourcesList[1])
            st.text(SourcesList[2])
