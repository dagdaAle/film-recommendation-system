import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Funzione per caricare i dati
def load_data(filepath):
    return pd.read_csv(filepath)

# Caricamento dei dati e costruzione delle matrici
movies_df = load_data('movies_processed.csv')
credits_df = load_data('credits_processed.csv')

# Unisci i due dataframe sul titolo del film
merged_df = pd.merge(movies_df, credits_df, on='title')

def get_homepage_from_csv(title):
    df = pd.read_csv("movies.csv-20231202T152800Z-001\movies.csv")
    movie_row = df.loc[df['title'].str.lower() == title.lower()].iloc[0]
    return movie_row['homepage']

# Funzione per combinare le caratteristiche in una singola stringa
def create_soup(features):
    return ' '.join([
        ' '.join(features['genres'].split()) if pd.notna(features['genres']) else '',
        ' '.join(features['keywords'].split()) if pd.notna(features['keywords']) else '',
        features['overview'] if pd.notna(features['overview']) else '',
        features['director'] if pd.notna(features['director']) else '',
        ' '.join(features['top_cast'].split()) if pd.notna(features['top_cast']) else ''
    ])

# Funzione per costruire la matrice TF-IDF
def build_tfidf_matrix(df):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    return tfidf_vectorizer.fit_transform(df['combined_features'])

def calculate_cosine_similarity(tfidf_matrix):
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crea una colonna combinata
merged_df['combined_features'] = merged_df.apply(create_soup, axis=1)

# Costruisci la matrice TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(merged_df['combined_features'])

# Calcola la similarità del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Funzione per raccomandare i film
def recommend_movies(title, df, cosine_sim):
    title = title.lower()
    if title not in df['title'].str.lower().values:
        return f"Film '{title}' non trovato. Per favore prova con un titolo diverso."

    idx = df.index[df['title'].str.lower() == title].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:5]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices]

def get_movie_details(movie_name, api_key):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    search_response = requests.get(search_url)
    if search_response.status_code == 200:
        search_data = search_response.json()
        if search_data['results']:
            first_result = search_data['results'][0]
            details_url = f"https://api.themoviedb.org/3/movie/{first_result['id']}?api_key={api_key}"
            details_response = requests.get(details_url)
            if details_response.status_code == 200:
                details_data = details_response.json()
                return {
                    'title': details_data['title'],
                    'image_url': "https://image.tmdb.org/t/p/w500" + details_data['poster_path'],
                    'rating': details_data['vote_average'],
                    'genres': ', '.join([genre['name'] for genre in details_data['genres']]),
                    'overview': details_data['overview'],
                    'release_date': details_data['release_date']
                }
    return None

# Esempio di utilizzo
# film_da_ricercare = input("Inserisci il titolo del film per ricevere raccomandazioni: ").lower()
# recommended_movies = recommend_movies(film_da_ricercare, merged_df, cosine_sim)
# print(recommended_movies)
