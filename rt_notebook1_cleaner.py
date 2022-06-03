#####
# the RT restart
# creating original dataframe files with "desktop" data and "mobile" data
# date: Jun 1st, 2022
# author: minjoon

#%%
# import all libraries
# from pickletools import long4
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
bdf_melted = bdf.melt(id_vars=['wid', 'timestamp'])
bdf_melted.sort_values(['wid', 'timestamp'], inplace=True)
bdf_melted.reset_index(drop=True, inplace=True)
bdf_melted.head()
# %%
# convert current data to 'analyzable' data... 
# new df = id(timestamp), movie, l/d, rt, watched
# all data in 4 row pairs.
# every 0: rating, 1: rt, 2: conf, 3: watched

df_B = pd.DataFrame(columns=['id', 'title', 'rating', 'rt', 'conf', 'watched'])
df_B['id'] = bdf_melted.iloc[::4]['timestamp']
df_B['title'] = bdf_melted.iloc[::4]['variable']
df_B['rating'] = bdf_melted.iloc[::4]['value']
df_B.reset_index(drop=True, inplace=True)

temp = bdf_melted.iloc[1::4]['value']
temp.reset_index(drop=True, inplace=True)
df_B['rt'] = temp 

temp = bdf_melted.iloc[2::4]['value']
temp.reset_index(drop=True, inplace=True)
df_B['conf'] = temp 

temp = bdf_melted.iloc[3::4]['value']
temp.reset_index(drop=True, inplace=True)
df_B['watched'] = temp 
# %%
# save original 'B' dataframe
df_B.to_csv('desktop_rt_data.csv', index=False)
# %%
# read in mobile data 
df_A = pd.read_csv('data/db_0504.csv')
df_A.head()
# %%
df_A = df_A[['uID', 'title', 'rating', 'time']]
df_A.rename({'uID': 'id', 'time': 'rt'}, axis=1, inplace=True)
df_A.head()
# %%
# save original 'A' dataframe
df_A.to_csv('mobile_rt_data.csv', index=False)
# %%
