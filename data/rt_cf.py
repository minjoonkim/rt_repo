#!usr/bin/python

"""
Implicit CF Recommender

created: Mar. 31st, 2021
author: Minjoon Kim
"""

# %%
# import libraries
import random
import pandas as pd
import numpy as np 

import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
from sklearn.preprocessing import MinMaxScaler

# %%
# DATA PREP

raw_data = pd.read_csv('db_0331_clean.csv')
data = raw_data.drop(raw_data.columns[0], axis=1)

data.head()
# %%
# convert movie titles and ratings to numerical IDs
data['movie_id'] = data['title'].astype("category").cat.codes
data['rating_cat'] = data['rating'].astype("category").cat.codes

# %%
# create a lookup frame to get movie titles from IDs
movie_lookup = data[['movie_id', 'title']].drop_duplicates()
movie_lookup = movie_lookup.movie_id.astype(str)

data = data.drop(['title'], axis=1)

# %%
users = list(np.sort(data.uID.unique()))
movies = list(np.sort(data.movie_id.unique()))
ratings = list(data.rating_cat)

# %%
# create user x movie matrix
df = pd.DataFrame(index=users, columns=movies)

for index, row in data.iterrows():
    a = row['uID']
    b = row['movie_id']
    c = row['rating_cat']

    df.loc[a][b] = c

# %%
# populate sparse matrix w/ ratings
df = df.replace(2, np.NaN)
data_sparse = sparse.csr_matrix(df.values)
