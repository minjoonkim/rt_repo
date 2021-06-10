"""
Machine learning model trial


Created: May 31st, 2021
@author: Minjoon
"""

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %%
# read in csv to dataframe
df = pd.read_csv('rt100_norm.csv')
# %%
# separate numerical/categorical columns
num_cols_df = df[['rt', 'rt_norm']]
cat_cols_df = df[['itemID', 'userID', 'rating']]
# %%
