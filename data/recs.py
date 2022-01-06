#%%
from sklearn import preprocessing
from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas_profiling as pp

#%%
df = pd.read_csv('user.csv')
# %%
df['rating'] = df['rating'] * (1/df['timestamp'])
# %%
df.to_csv('userfix.csv')
# %%
