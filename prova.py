import pandas as pd

def get_homepage_from_csv(title):
    df = pd.read_csv("movies.csv-20231202T152800Z-001\movies.csv")
    movie_row = df.loc[df['title'].str.lower() == title.lower()].iloc[0]
    return movie_row['homepage']

print(get_homepage_from_csv("Pirates of the Caribbean: At World's End"))
