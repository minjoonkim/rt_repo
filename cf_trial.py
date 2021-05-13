#####
# Memory-based CF Tutorial
# Created: 2020/10/05
# https://blog.cambridgespark.com/nowadays-recommender-systems-are-used-to-personalize-your-experience-on-the-web-telling-you-what-120f39b89c3c
# Memory-based user-item & item-item collaboraive filtering implementation

#%% import numpy and pandas
import numpy as np
import pandas as pd

#%% read in data file
header = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('ml-100k/u.data', sep='\t', names=header)

#%% 
n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]

print("Number of users: " + str(n_users) + " | Number of movies: " + str(n_items))
#%% import sklearn, train_test_split
from sklearn import model_selection

train_data, test_data = model_selection.train_test_split(df, test_size=0.25, random_state=42)

#%% create two user-item matrices, one for training and another for testing
train_data_matrix = np.zeros((n_users, n_items))
for line in train_data.itertuples():
    train_data_matrix[line[1]-1, line[2]-1] = line[3]


test_data_matrix = np.zeros((n_users, n_items))
for line in test_data.itertuples():
    test_data_matrix[line[1]-1, line[2]-1] = line[3]

#%% create two user-item matrices, one for training and another for testing

sparsity = round(1.0 - len(df) / float(n_users*n_items), 3)
print('The sparsity of MovieLens 100K: ' + str(sparsity*100) + '%')

#%% make rsme function
from sklearn.metrics import mean_squared_error
from math import sqrt

def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()

    return sqrt(mean_squared_error(prediction, ground_truth))

#%% 
import scipy.sparse as sp
from scipy.sparse.linalg import svds

# get SVD components from train matrix. Choose k
u, s, vt = svds(train_data_matrix, k = 20)
s_diag_matrix = np.diag(s)
X_pred = np.dot(np.dot(u, s_diag_matrix), vt)

print('User-based CF MSE: ' + str(rmse(X_pred, test_data_matrix)))

# %%
