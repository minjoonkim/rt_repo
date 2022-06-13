#####
# rt notebook #3: statistical analysis
# 1. finding the relation between confidence and RT in desktop
# 2. checking if the desktop rt data can be used with mobile rt data

# %% import libraries
import pandas as pd
import numpy as np
import seaborn as sns


# %%
# read in data
rtd = pd.read_csv('desktop_rt_data_lognorm.csv')
rtm = pd.read_csv('mobile_rt_data_lognorm.csv')

# %%
# descriptive stats for like/dislike/skip ratings
dskip = rtd[rtd.rating == 'skip']
dlike = rtd[rtd.rating == 'like']
ddislike = rtd[rtd.rating == 'dislike']

print("like:", len(dlike), "dislike:", len(ddislike), "skip:", len(dskip))
# %%
dskip['rt'].mean()
dlike['rt'].mean()
ddislike['rt'].mean()
# %%
