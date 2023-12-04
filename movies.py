import pandas as pd
import json

# Load the movies dataset
movies_df = pd.read_csv('movies.csv-20231202T152800Z-001\movies.csv')

# Function to convert JSON string to a list of dictionaries
def load_json(data):
    return json.loads(data)

# Convert JSON strings in 'genres' and 'keywords' columns to lists of dictionaries
movies_df['genres'] = movies_df['genres'].apply(load_json)
movies_df['keywords'] = movies_df['keywords'].apply(load_json)

# Extract names from the genres and keywords
def extract_names(data):
    return ' '.join([item['name'] for item in data])

movies_df['genres'] = movies_df['genres'].apply(extract_names)
movies_df['keywords'] = movies_df['keywords'].apply(extract_names)

# Select the columns of interest
processed_movies_df = movies_df[['title', 'genres', 'keywords', 'overview']]

# Save the results to a new CSV file
output_file_path = 'movies_processed.csv'
processed_movies_df.to_csv(output_file_path, index=False)

print(f"The data has been saved in {output_file_path}")
