#############
# response time adjustment on MovieLens dataset
# created: May 20th, 2021
# author: minjoon

# %%
# import libraries
import pandas as pd
import numpy as np

# %%
# read in data set

ratings = pd.read_csv('ml-latest-small/ratings.csv')

ratings_dict = {'itemID': list(ratings.movieId),
                'userID': list(ratings.userId),
                'rating': list(ratings.rating),
                'timestamp': list(ratings.timestamp)}

df = pd.DataFrame(ratings_dict)

# %%
# sort by users and timestamp
df = df.sort_values(['userID', 'timestamp'])

#%%
# calculate response times and save as df column
df['rt'] = 0
df['rt'] = df['timestamp'] - df['timestamp'].shift(1)

# %%
# get first ratings of each user
firsts = df.groupby('userID').first()

# %%
# get rid of first ratings (no RTs)
# outer merge subset df (firsts) to original df, drop rows with 'both' merge tags
out = pd.merge(df, firsts, how='outer', indicator=True)
df = out[out._merge.ne('both')].drop('_merge', 1)

# %%
# df cleaning. reset index and make userID as int
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
df = df.astype({"userID": int})

# %%
# get rid of ratings that take too long.
# initial cut-off: 100 seconds (about 10% of data points lost)
df100 = df[df.rt < 101]
df100.to_csv('rt100.csv')
# %%
