#####
# CF Movie Recommender from implicit feedback
# Created: 2020/10/07
# https://medium.com/analytics-vidhya/implementation-of-a-movies-recommender-from-implicit-feedback-6a810de173ac

#%% import needed libraries

import os
import sys
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, save_npz, load_npz, vstack, hstack, lil_matrix
import implicit
import pickle
from implicit.evaluation import train_test_split, precision_at_k, mean_average_precision_at_k

#%% load data from python 25m dataset
def load_data():
    '''load the MovieLens 1m dataset in a Pandas dataframe'''
    ratings = pd.read_csv('ml-1m/ratings.dat', delimiter='::', header=None,
                          names=['user_id', 'movie_id', 'rating', 'timestamp'],
                          usecols=['user_id', 'movie_id', 'rating'], engine='python')

    return ratings

#%%
def sparse_matrices(df):
    '''creates the sparse user-item and item-user matrices'''

    # using a scalar value (40) to convert ratings from a scale (1-5) to a like/click/view (1)
    alpha = 40

    sparse_user_item = csr_matrix(
        ([alpha]*len(df['movie_id']), (df['user_id'], df['movie_id'])))
    # transposing the item-user matrix to create a user-item matrix
    sparse_item_user = sparse_user_item.T.tocsr()
    # save the matrices for recalculating user on the fly
    save_npz("sparse_user_item.npz", sparse_user_item)
    save_npz("sparse_item_user.npz", sparse_item_user)

    return sparse_user_item, sparse_item_user
