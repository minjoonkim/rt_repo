##########
# visualization for MovieLens Latest Small dataset
# created: May 21st, 2021
# author: minjoon

# %%
# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from seaborn import palettes

from sklearn import preprocessing

# %%
# read in csv, drop additional index (should have used index=False haha)
df = pd.read_csv('rt100.csv')
df.drop(df.columns[0], axis=1)

# %%
# normalize response times
ids = df.userID.unique()

for uid in ids:
    # get rts per UID
    x = df.loc[df['userID'] == uid]['rt']
    x = x.values.astype(float)
    x = x.reshape(-1, 1)
    scaler = preprocessing.MinMaxScaler()

    # create scaler
    x_scaled = scaler.fit_transform(x)

    # get index
    idx = df[df['userID'] == uid].index.values.astype(int)[0]

    df.loc[df['userID'] == uid, 'rt_norm'] = x_scaled
# %%
# get all ratings and sort ascending
orig_ratings = df.rating.unique()
orig_ratings = np.sort(orig_ratings)

# %%
# distplot version - plot each ratings based on normalized rating time
for rating in orig_ratings:
    plt.figure()
    plt.title(rating)
    sns.distplot(df.loc[(df['rating'] == rating)]['rt_norm'])


# %%
# histplot version - plot each ratings based on normalized rating time
sns.histplot(data=df[['rating', 'rt_norm']], x="rt_norm", hue="rating", palette="colorblind")

# %%
