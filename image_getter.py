import requests

def get_movie_details(movie_name, api_key):
    # Ricerca del film per nome
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    search_response = requests.get(search_url)
    if search_response.status_code == 200:
        search_data = search_response.json()
        if search_data['results']:
            first_result = search_data['results'][0]
            movie_id = first_result['id']

            # Richiesta dettagli specifici del film
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
            details_response = requests.get(details_url)
            if details_response.status_code == 200:
                details_data = details_response.json()
                return {
                    'title': details_data['title'],
                    'image_url': "https://image.tmdb.org/t/p/w500" + details_data['poster_path'],
                    'rating': details_data['vote_average'],
                    'genres': ', '.join([genre['name'] for genre in details_data['genres']]),
                    'overview': details_data['overview'],
                    'release_date': details_data['release_date'],
                    # Aggiungi qui altre informazioni se necessario
                }
    return None

# Esempio di utilizzo
api_key = "460f652be13cda73859b2d2b68f6154e"
movie_details = get_movie_details("Blade: Trinity", api_key)
print(movie_details)
