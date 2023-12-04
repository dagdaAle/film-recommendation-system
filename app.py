from flask import Flask, render_template, request, jsonify
import raccomandation_system as recommender
import pandas as pd
import image_getter
import requests

app = Flask(__name__)

# Carica i dati e prepara la matrice di similarità
movies_df = recommender.load_data('movies_processed.csv')
credits_df = recommender.load_data('credits_processed.csv')
merged_df = pd.merge(movies_df, credits_df, on='title')
merged_df['combined_features'] = merged_df.apply(recommender.create_soup, axis=1)

tfidf_matrix = recommender.build_tfidf_matrix(merged_df)
cosine_sim = recommender.calculate_cosine_similarity(tfidf_matrix)


@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            recommended_titles = recommender.recommend_movies(title, merged_df, cosine_sim)
            recommendations = [recommender.get_movie_details(title, '460f652be13cda73859b2d2b68f6154e') for title in recommended_titles]
            for movie in recommendations:
                movie['homepage'] = recommender.get_homepage_from_csv(movie['title'])

    return render_template('index.html', movies=recommendations)

@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('q', '')
    suggestions = merged_df[merged_df['title'].str.contains(query, case=False)]['title'].tolist()
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
