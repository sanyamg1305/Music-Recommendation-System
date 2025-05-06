# recommender.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

# Load the data (ensure 'data.csv' is in the same directory as this script)
df = pd.read_csv('data.csv')

# Preprocess and standardize features
audio_features = ['valence', 'acousticness', 'danceability', 'duration_ms',
                  'energy', 'instrumentalness', 'key', 'liveness',
                  'loudness', 'mode', 'popularity', 'speechiness', 'tempo', 'year']

scaler = StandardScaler()
content_scaled = scaler.fit_transform(df[audio_features])

# Fit NearestNeighbors model for content-based recommendations
nn_model_content = NearestNeighbors(n_neighbors=11, metric='cosine', algorithm='brute')
nn_model_content.fit(content_scaled)

# Collaborative filtering setup
top_songs_df = df.sort_values('popularity', ascending=False).drop_duplicates('name').head(10000)
top_songs_df = top_songs_df[['name', 'popularity']].copy()

# Simulate user interactions
top_songs_df = pd.concat([top_songs_df] * 3, ignore_index=True)
top_songs_df['user_id'] = top_songs_df.index % 5000

grouped_df = top_songs_df.groupby(['user_id', 'name']).agg({'popularity': 'mean'}).reset_index()
pivot_df = grouped_df.pivot(index='user_id', columns='name', values='popularity').fillna(0)
sparse_matrix = csr_matrix(pivot_df.values)

model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(sparse_matrix)

def get_content_recommendations(song_name, top_n=5):
    idx_list = df[df['name'].str.lower() == song_name.lower()].index
    if idx_list.empty:
        return "Sorry, we couldn't find the track. Try again with a different song!"
    
    idx = idx_list[0]
    distances, indices = nn_model_content.kneighbors([content_scaled[idx]], n_neighbors=top_n+1)
    rec_indices = indices[0][1:]
    
    return df.iloc[rec_indices][['name', 'artists', 'popularity']]

def get_collab_recommendations(song_name, top_n=5):
    if song_name not in pivot_df.columns:
        return "Sorry, we couldn't find the track. Try again with a different song!"
    
    song_idx = pivot_df.columns.get_loc(song_name)
    song_vector = pivot_df.T.iloc[song_idx].values.reshape(1, -1)
    
    distances, indices = model_knn.kneighbors(song_vector, n_neighbors=top_n+1)
    rec_indices = indices.flatten()[1:]
    rec_songs = pivot_df.columns[rec_indices]
    
    return df[df['name'].isin(rec_songs)][['name', 'artists', 'popularity']].drop_duplicates()

def recommend(song_name, method='content', top_n=5):
    if method == 'content':
        return get_content_recommendations(song_name, top_n)
    elif method == 'collab':
        return get_collab_recommendations(song_name, top_n)
    else:
        return "Method must be either 'content' or 'collab'."
