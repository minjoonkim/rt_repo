#!usr/bin/python

"""
Analysis file for individual performance on RT

created: Mar. 31st, 2021
author: Minjoon Kim
"""

# %%
# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import shapiro

# %%
# read csv
df = pd.read_csv('db_0331_clean.csv')

df.head()
# %%
# skip vs like vs dislike
skip_rt = df.loc[df['rating'] == 'skip']['time'].mean()
like_rt = df.loc[df['rating'] == 'like']['time'].mean()
dislike_rt = df.loc[df['rating'] == 'dislike']['time'].mean()

print("skip rt: ", skip_rt)
print("like rt: ", like_rt)
print("dislike rt: ", dislike_rt, "\n")

# %%
# average skip per individual data
ids = df.uID.unique()

for uid in ids:
    skip_avg = df.loc[(df['uID'] == uid) & (
        df['rating'] == 'skip')]['time'].mean()
    like_avg = df.loc[(df['uID'] == uid) & (
        df['rating'] == 'like')]['time'].mean()
    dislike_avg = df.loc[(df['uID'] == uid) & (
        df['rating'] == 'dislike')]['time'].mean()

    skip_med = df.loc[(df['uID'] == uid) & (
        df['rating'] == 'skip')]['time'].median()
    like_med = df.loc[(df['uID'] == uid) & (
        df['rating'] == 'like')]['time'].median()
    dislike_med = df.loc[(df['uID'] == uid) & (
        df['rating'] == 'dislike')]['time'].median()

    print(uid, "skip_avg: ", skip_avg, "skip_med: ", skip_med)
    print(uid, "like_avg: ", like_avg, "like_med: ", like_med)
    print(uid, "dislike_avg: ", dislike_avg, "dislike_med: ", dislike_med, "\n")

# %%
df['rt_seconds'] = df['time'].div(1000)

# %%
rts = sns.displot(df, x="rt_seconds", hue="rating")


# %%
# skew test
skip_skew = df.loc[df['rating'] == 'skip']['time'].skew()
like_skew = df.loc[df['rating'] == 'like']['time'].skew()
dislike_skew = df.loc[df['rating'] == 'dislike']['time'].skew()

print ("skip skew:", skip_skew)
print ("like skew:", like_skew)
print("dislike skew:", dislike_skew)


# %%
