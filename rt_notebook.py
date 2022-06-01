#####
# the RT restart
# rt + skip with "desktop" data and "mobile" data

#%%
# import all libraries
import pandas as pd 
import numpy as np 
import seaborn as sns 

#%%
# read in desktop data
bdata = pd.read_csv('data/data_B.csv')
bdata.head()
# %%
# cleaning: change timestamp datatype
bdata['timestamp'] = pd.to_datetime(bdata['timestamp'])
bdata.head()
#%%
# cleaning: change 'timestamp' to actual timestamp
bdata['timestamp'] = bdata.timestamp.values.astype(np.int64) // 10 ** 9
bdata.head()
# %%
# remove test cases and remove email column
bdf = bdata.iloc[2:]
bdf = bdf.drop('email', axis=1)
bdf.head()
# %%
# make wide-format in to long-format
df_melted = bdf.melt(id_vars=['wid', 'timestamp'])
df_melted.sort_values(['wid', 'timestamp'], inplace=True)
df_melted.head()
# %%
# convert current data to 'analyzable' data... 
# id(timestamp), movie, l/d, rt, watched
# movie = does not include '_'
# l/d = like, dislike, or dunno 
# rt = float
# watched = watched or not
