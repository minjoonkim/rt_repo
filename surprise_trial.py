#####
# CF Movie Recommender with Scikit Surprise package
# Created: 2021/05/14
# Author: minjoon

#%%
# import libraries

import pandas as pd

from surprise import Reader, Dataset
from surprise import SVD
from surprise import NMF

from surprise.model_selection import KFold
from surprise.model_selection import cross_validate


#%%
# read in dataset to pandas df
ratings = pd.read_csv('ml-latest-small/ratings.csv')

ratings_dict = {'itemID': list(ratings.movieId),
                'userID': list(ratings.userId),
                'rating': list(ratings.rating)}

df = pd.DataFrame(ratings_dict)

# a reader is still needed but only the rating_scale param is required.
# the reader class is used to parse a file conataining ratings.
reader = Reader(rating_scale=(0.5, 5.0))

# the colums must correspond to user id, item id, and ratings

data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)


#%%
# split data into 5 folds

kf = KFold(n_splits=5)
kf.split(data)


#%%
# singular value decomposition (SVD)
algo = SVD()
cross_validate(algo, data)

#%%
# non-negative matrix factorization (NMF)
algo = NMF()
cross_validate(algo, data)

# %%
