# recommender.py

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

# Load your dataset
data = pd.read_csv("data.csv")

# Select numerical columns for clustering
X = data.select_dtypes(np.number)
number_cols = list(X.columns)

# Fit KMeans clustering (for internal structure – optional but used in your notebook)
song_cluster_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('kmeans', KMeans(n_clusters=20, verbose=False))
])
song_cluster_pipeline.fit(X)
data['cluster_label'] = song_cluster_pipeline.predict(X)

# Recommendation function
def recommend(song_title, n_recommendations=5):
    if song_title not in data['name'].values:
        return []

    song_index = data[data['name'] == song_title].index[0]
    song_features = data.loc[song_index, number_cols].values.reshape(1, -1)
    song_features = song_features.astype(float)

    numeric_data = data[number_cols].apply(pd.to_numeric, errors='coerce').fillna(0).values
    distances = cdist(song_features, numeric_data, metric='euclidean')
    similar_indices = distances.argsort()[0][1:n_recommendations + 1]
    
    return data.loc[similar_indices, 'name'].tolist()
