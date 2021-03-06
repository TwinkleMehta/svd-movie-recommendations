import numpy as np 
import pandas as pd 

# Reading dataset (MovieLens 1M movie ratings dataset: downloaded from https://grouplens.org/datasets/movielens/1m/)
data = pd.io.parsers.read_csv('data/ratings.dat', 
    names=['user_id', 'movie_id', 'rating', 'time'],
    engine='python', delimiter='::')
movie_data = pd.io.parsers.read_csv('data/movies.dat',
    names=['movie_id', 'title', 'genre'],
    engine='python', delimiter='::')

# Reading test dataset (testMovies and testRatings)
# data = pd.io.parsers.read_csv('data/testRatings.dat', 
#     names=['user_id', 'movie_id', 'rating', 'time'],
#     engine='python', delimiter='::')
# movie_data = pd.io.parsers.read_csv('data/testMovies.dat',
#     names=['movie_id', 'title', 'genre'],
#     engine='python', delimiter='::')

# Creating the rating matrix (rows as movies, columns as users)
ratings_mat = np.ndarray(
    shape=(np.max(data.movie_id.values), np.max(data.user_id.values)),
    dtype=np.uint8)
ratings_mat[data.movie_id.values-1, data.user_id.values-1] = data.rating.values

# Normalizing the matrix(subtract mean off)
normalised_mat = ratings_mat - np.asarray([(np.mean(ratings_mat, 1))]).T
# Computing the Singular Value Decomposition (SVD)
A = normalised_mat.T / np.sqrt(ratings_mat.shape[0] - 1)
U, S, V = np.linalg.svd(A)
# print("U from SVD: ", U)
# print("S from SVD: ", S)
# print("VT from SVD: ", V)

# Function to calculate the cosine similarity (sorting by most similar and returning the top N)
def top_cosine_similarity(data, movie_id, top_n=10):
    index = movie_id - 1 # Movie id starts from 1 in the dataset
    movie_row = data[index, :]
    magnitude = np.sqrt(np.einsum('ij, ij -> i', data, data))
    similarity = np.dot(movie_row, data.T) / (magnitude[index] * magnitude)
    sort_indexes = np.argsort(-similarity)
    np.seterr(divide='ignore', invalid='ignore')
    return sort_indexes[:top_n+1] # add 1, because top is same movie

# Function to print top N similar movies
def print_similar_movies(movie_data, movie_id, top_indexes):
    print('Recommendations for {0}: \n'.format(
    movie_data[movie_data.movie_id == movie_id].title.values[0]))
    for id in top_indexes + 1:
        if movie_id != id: # exclude same movie
            print(movie_data[movie_data.movie_id == id].title.values[0])
            print(movie_data[movie_data.movie_id == id].genre.values , '\n')

# k-principal components to represent movies, movie_id to find recommendations, top_n print n results        
k = 30 # PCA Analysis
movie_id = 2 # (getting an id from movies.dat)
top_n = 15
sliced = V.T[:, :k] # representative data
indexes = top_cosine_similarity(sliced, movie_id, top_n)

# Printing the top N similar movies
print("Principal components representd (K) = ", k)
print_similar_movies(movie_data, movie_id, indexes)