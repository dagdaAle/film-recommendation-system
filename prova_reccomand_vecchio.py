import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import matplotlib.pyplot as plt
import seaborn as sns

import networkx as nx
import matplotlib.pyplot as plt

# Usa la funzione per creare e visualizzare il grafo

import networkx as nx
import plotly.graph_objs as go
from plotly.offline import plot

def create_interactive_network(cosine_sim, movies_df, top_n=50):
    # Crea il grafo
    G = nx.Graph()
    
    # Aggiungi i nodi con i titoli dei film
    nodes = movies_df['title'][:top_n]
    G.add_nodes_from(nodes)
    
    # Aggiungi gli archi tra i nodi se la similarità supera una certa soglia
    for i in range(top_n):
        for j in range(i + 1, top_n):
            if cosine_sim[i][j] > 0.08:  # Soglia di similarità
                G.add_edge(nodes[i], nodes[j], weight=cosine_sim[i][j])

    # Posizione dei nodi con spring layout
    pos = nx.spring_layout(G)

    # Creazione degli edge traces
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    # Creazione dei node traces
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=[],
            opacity=0.8,
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([node])

    # Colora i nodi in base al grado dei nodi
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])

    # Crea la figura
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0,l=0,r=0,t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Mostra la figura
    plot(fig)




# Funzione per caricare i dati
def load_data(filepath):
    movies_df = pd.read_csv(filepath)
    movies_df['overview'] = movies_df['overview'].fillna('')
    return movies_df

# Funzione per costruire la matrice TF-IDF
def build_tfidf_matrix(movies_df):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['overview'])
    return tfidf_matrix

# Funzione per calcolare la similarità del coseno
def calculate_cosine_similarity(tfidf_matrix):
    return cosine_similarity(tfidf_matrix, tfidf_matrix)
    

# Funzione per raccomandare i film
def recommend_movies(title, movies_df, cosine_sim):
    title = title.lower()
    if title not in movies_df['title'].str.lower().values:
        return f"Film '{title}' non trovato. Per favore prova con un titolo diverso."

    idx = movies_df.index[movies_df['title'].str.lower() == title].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies_df['title'].iloc[movie_indices]

# Percorso del file (aggiusta secondo il tuo ambiente)
file_path = 'movies.csv-20231202T152800Z-001\movies.csv'
# Carica i dati dei crediti

credits_df = pd.read_csv('credits.csv-20231202T112951Z-001/credits.csv')

# Caricamento dei dati e costruzione delle matrici
movies_df = load_data(file_path)
tfidf_matrix = build_tfidf_matrix(movies_df)
cosine_sim = calculate_cosine_similarity(tfidf_matrix)

# Input dell'utente e raccomandazione
#film_da_ricercare = input("Inserisci il titolo del film per ricevere raccomandazioni: ").lower()
#recommended_movies = recommend_movies(film_da_ricercare, movies_df, cosine_sim)
#print(recommended_movies)

# Chiamata alla funzione
create_interactive_network(cosine_sim, movies_df, top_n=1000)