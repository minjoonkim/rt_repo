#%%
from sklearn import preprocessing
from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas_profiling as pp

#%%
df = pd.read_csv('db_0504_clean.csv')

# %%
# log-normalized response times
ids = df.uID.unique()
for uid in ids:
    # get rts per UID
    x = df.loc[df['uID'] == uid]['time']
    x = x.values.astype(float)
    x = x.reshape(-1, 1)
    scaler = preprocessing.MinMaxScaler()

    # create scaler
    x_scaled = scaler.fit_transform(x)

    # get index
    idx = df[df['uID'] == uid].index.values.astype(int)[0]

    df.loc[df['uID'] == uid, 'rtlognorm'] = x_scaled

# %%
c1 = df['time'].loc[df['rating'] == 'skip']
c2 = df['time'].loc[df['rating'] == 'like']
c5 = df['time'].loc[df['rating'] == 'dislike']

n1 = df['rtlognorm'].loc[df['rating'] == 'skip']
n2 = df['rtlognorm'].loc[df['rating'] == 'like']
n5 = df['rtlognorm'].loc[df['rating'] == 'dislike']

# %%
color = sns.set_palette("colorblind", n_colors=3, color_codes=True)
fig, axes = plt.subplots(1, 3, figsize=(20, 5))
fig.subplots_adjust(hspace=1.5, wspace=1.5)

p1 = fig.add_subplot(1, 3, 1)
fig.tight_layout()
p1.set_title('Skip')
sns.distplot(c1, color="b")
p1.tick_params(bottom=False, left=False)
p1.set(xticklabels=[], yticklabels=[], xlabel='rtlognorm')

p2 = fig.add_subplot(1, 3, 2)
fig.tight_layout()
p2.set_title('Like')
sns.distplot(c2, color="g")
p2.tick_params(bottom=False, left=False)
p2.set(xticklabels=[], yticklabels=[], xlabel='rtlognorm')

p5 = fig.add_subplot(1, 3, 3)
fig.tight_layout()
p5.set_title('Dislike')
sns.distplot(c5, color="r")
p5.tick_params(bottom=False, left=False)
p5.set(xticklabels=[], yticklabels=[], xlabel='rtlognorm')

# %%
plt.rcParams['figure.figsize'] = (10, 5)


# %%
sns.ecdfplot(data=n1, legend="Skip")
sns.ecdfplot(data=n2, legend="Like")
sns.ecdfplot(data=n5, legend="Dislike")




# %%
