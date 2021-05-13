#####
# CF Movie Recommender from binary data
# Created: 2020/10/07
# https://medium.com/radon-dev/item-item-collaborative-filtering-with-binary-or-unary-data-e8f0b465b2c3

#%%
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from scipy.sparse import csr_matrix

#%%
# read in data from u.data file
header = ['user_id', 'item_id', 'rating', 'timestamp']

ratings = pd.read_csv('ml-latest-small/ratings.csv', names=header, skiprows=[0])
movies = pd.read_csv('ml-latest-small/movies.csv')

#%%
# how many users & how many movies?
users = ratings.user_id.unique().shape[0]
items = ratings.item_id.max()

print("Number of users: " + str(users) + " | Number of movies: " + str(items))

#%%
# create user-item sparse matrix, make it into a dataframe
ui_sparse = np.zeros((users, items))

for line in ratings.itertuples():
    ui_sparse[line[1]-1, line[2]-1] = line[3]

data_items = pd.DataFrame(ui_sparse)
data_items = data_items.loc[:, (data_items != 0).any(axis=0)]

#%%
#-----------------------
# item-item calculations
#-----------------------

# as a first step we normalize the user vectors to unit vectors

#magnitude = sqrt(x2 + y2 + z2 + ...)
magnitude = np.sqrt(np.square(data_items).sum(axis=1))

# unitvector = (x/magnitude, y/magnitude, z/magnitude, ...)
data_items = data_items.divide(magnitude, axis='index')

def calculate_similarity(data_items):
    """
    Calculate the column-wise cosine similarity for a sparse matrix.
    Return a new dataframe matrix with similarities
    """
    data_sparse = sparse.csr_matrix(data_items)
    similarities = cosine_similarity(data_sparse.transpose())
    sim = pd.DataFrame(data=similarities, index=data_items.columns, columns=data_items.columns)
    return sim

# build the similarity matrix
data_matrix = calculate_similarity(data_items)

#%%
print(data_matrix.loc[122905].nlargest(11))
print(movies[movies['movieId'] == 122906]['title'])
# %%
#------------------------
# USER-ITEM CALCULATIONS
#------------------------

user = 609  # The id of the user for whom we want to generate recommendations
user_index = ratings[ratings.user_id == user].index.tolist()[0]  # Get the frame index

# Get the artists the user has liked.
known_user_likes = data_items.iloc[user_index]
known_user_likes = known_user_likes[known_user_likes > 0].index.values

# Users likes for all items as a sparse vector.
user_rating_vector = data_items.iloc[user_index]

# Calculate the score.
score = data_matrix.dot(user_rating_vector).div(data_matrix.sum(axis=1))

# Remove the known likes from the recommendation.
score = score.drop(known_user_likes)

# Print the known likes and the top 20 recommendations.
print(known_user_likes)
print(score.nlargest(10))


# %%
