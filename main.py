import streamlit as st
import pandas as pd
import io

def merge_data(queries_file, search_volume_file):
    # Daten aus den hochgeladenen Dateien laden
    queries_df = pd.read_csv(queries_file)
    search_volume_df = pd.read_csv(search_volume_file, encoding='UTF-16', delimiter='	', skiprows=2)
    
    # Überprüfen, ob die erforderlichen Spalten vorhanden sind
    if "Top queries" not in queries_df.columns:
        st.error("Die Datei muss eine Spalte 'Top queries' enthalten.")
        return
    if "Keyword" not in search_volume_df.columns or "Avg. monthly searches" not in search_volume_df.columns:
        st.error("Die Datei muss die Spalten 'Keyword' und 'Avg. monthly searches' enthalten.")
        return
    
    # Merge der Daten
    merged_df = queries_df.merge(search_volume_df[['Keyword', 'Avg. monthly searches']], 
                                 left_on='Top queries', right_on='Keyword', how='left')
    
    # Löschen der "Keyword"-Spalte nach dem Merge
    merged_df = merged_df.drop(columns='Keyword')
    
    return merged_df

st.title("Monthly Search Volume Hinzufügen")

# Upload-Buttons für die Dateien
queries_file = st.file_uploader("Laden Sie die erste CSV-Datei hoch (sollte 'Top queries' enthalten)", type=["csv"])
search_volume_file = st.file_uploader("Laden Sie die zweite CSV-Datei hoch (sollte 'Keyword' und 'Avg. monthly searches' enthalten)", type=["csv"])

# Wenn beide Dateien hochgeladen wurden und der Button geklickt wird
if queries_file and search_volume_file and st.button("Add monthly search volume to GSC data"):
    merged_df = merge_data(queries_file, search_volume_file)
    
    # Wenn merged_df nicht None ist (was bedeutet, dass es keine Fehler gab), erstellen Sie einen herunterladbaren Link
    if merged_df is not None:
        csv = merged_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="updated_queries.csv">Download updated CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
