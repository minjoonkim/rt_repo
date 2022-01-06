#!/user/bin/python

"""
Data Cleaner
creation date: 03.25.2021

how to run:
python cleaner.py file_name
ex) python cleaner.py db_0325.csv

outputs a csv file based on ID & rating order.
only completed ratings (at least 40 movies) are included in the final csv,
with the first rating of each user gone for load/sync issues with timer
"""

# %% 
# import libraries
import pandas as pd 
import sys
import os

# %% 
# read csv 
inFile = sys.argv[1]
data = pd.read_csv(inFile)

data.head()

# %%
# sort out "test" entries
# = drop rows with uID counts less than 30
data = data.rename_axis('index').sort_values(
    by=['uID', 'index'])

data.head()

# %%
data = data.groupby('uID').filter(lambda x: len(x) > 40)
ids = data.uID.unique()
df = pd.DataFrame()

print("unique ids: ", len(ids))
for uid in ids:
    print(uid)
    temp = data.loc[data['uID'] == uid][1:]
    df = df.append(temp)

# %%
# clean duplicates
df = df.drop_duplicates(subset=['uID', 'title'])
df = df.reset_index(drop=True)
# df.drop(df.columns[0], axis=1)

# %%
# clean impossible ratings
df = df.drop(df[df.time < 100].index)
df = df.drop(df[df.time > 30000].index)
df = df.reset_index(drop=True)

# %%
# skip vs like vs dislike
skip_rt = df.loc[df['rating'] == 'skip']['time'].mean()
like_rt = df.loc[df['rating'] == 'like']['time'].mean()
dislike_rt = df.loc[df['rating'] == 'dislike']['time'].mean()

# %%
print("skip rt: ", skip_rt)
print("like rt: ", like_rt)
print("dislike rt: ", dislike_rt, "\n")


# %% 
# save to .csv file
outFile = os.path.splitext(inFile)[0]
df.to_csv(outFile + '_clean1.csv')
print("wrote to " + outFile + "_clean1.csv")
print("done..!")

# %%
