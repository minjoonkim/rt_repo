#####
# the RT restart
# rt + skip with "desktop" data and "mobile" data

#%%
# import all libraries
from pickletools import long4
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


# %%
# google interview question re-do
data = {'Year': [2022, 2021, 2020, 2019],
        'Jan': [20, 21, 19, 18], 
        'Feb': [20, 21, 19, 18],
        'Mar': [20, 21, 19, 18],
        'Apr': [20, 21, 19, 18],
        'May': [20, 21, 19, 18],
        'Jun': [20, 21, 19, 18],
        'Jul': [20, 21, 19, 18],
        'Aug': [20, 21, 19, 18],
        'Sep': [20, 21, 19, 18],
        'Oct': [20, 21, 19, 18],
        'Nov': [20, 21, 19, 18],
        'Dec': [20, 21, 19, 18],
        }

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

wide = pd.DataFrame(data)
wide 
# %%
# long format check
long = wide.melt(id_vars=['Year'], var_name='Month', value_name='Value')
long
# %%
# sort by year and month?
long['Month'] = pd.Categorical(long['Month'], categories=months, ordered=True)
long.sort_values(['Year', 'Month'], ascending=[False, True], inplace=True)
long.reset_index(inplace=True, drop=True)
long

# %%
