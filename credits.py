import pandas as pd
import json

# Carica i dati dei crediti
credits_df = pd.read_csv('credits.csv-20231202T112951Z-001/credits.csv')

# Funzione per convertire JSON in lista di dizionari
def load_json(data):
    return json.loads(data)

# Converti le stringhe JSON in liste di dizionari
credits_df['cast'] = credits_df['cast'].apply(load_json)
credits_df['crew'] = credits_df['crew'].apply(load_json)

# Funzione per estrarre il nome del regista
def get_director(crew_data):
    for crew_member in crew_data:
        if crew_member['job'] == 'Director':
            return crew_member['name']
    return None

# Applica la funzione per ottenere il nome del regista
credits_df['director'] = credits_df['crew'].apply(get_director)

# Estrai i nomi dei primi 3 membri del cast
def get_top_cast_names(cast_data, top_n=5):
    if cast_data:
        return ' '.join([member['name'] for member in cast_data[:top_n]])
    return ''

credits_df['top_cast'] = credits_df['cast'].apply(lambda x: get_top_cast_names(x))

# Rimuovi le colonne originali 'cast' e 'crew'
credits_df = credits_df.drop(columns=['cast', 'crew'])

# Salva i risultati in un nuovo file CSV
output_file_path = 'credits_processed.csv'
credits_df.to_csv(output_file_path, index=False)

print(f"I dati sono stati salvati in {output_file_path}")
