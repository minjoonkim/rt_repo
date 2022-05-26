#########
# data wrangling exercise #2
# created: May 25th, 2022
# author: minjoon


#%% all imports
from inspect import stack
import requests
from bs4 import BeautifulSoup
from IPython.core.display import HTML

import pandas as pd 

#%%
req = requests.get('https://en.wikipedia.org/wiki/Harvard_University')
print(req)

# %%
# take a look at the structure of the 'dir' of the requests
dir(req)
# %%
page = req.text
print(page)
# %%
soup = BeautifulSoup(page, 'html.parser')
soup
# %%
# compare type of page and soup
type(page)
#%%
type(soup)
# %%
# prettifying beautifulsoup
print(soup.prettify())
# %%
soup.title
# %%
"title" in soup.title
# %%
len(soup.findAll('p'))

# %%
soup.table["class"]
# %%
# list comprehension
# we will see if all the tables have a 'class' attribute. 
[t["class"] for t in soup.find_all("table") if t.get("class")]
# %%
# example using the 'Demographics' table from the HU wiki page
table_html = str(soup.find_all("table", "wikitable")[3])
HTML(table_html)
# %%
# using list comprehension to extract the rows (tr) elements
rows = [row for row in soup.find_all("table", "wikitable")[3].find_all("tr")]
rows
# %%
# lambda expressions 
# example with replacing newline with spaces
remove_nl = lambda s: s.replace("\n", "")

# %%
# extracting text in columns
columns = [remove_nl(col.get_text()) for col in rows[0].find_all('th') if col.get_text()]
columns
# %%
# extracting text in rows
indexes = [remove_nl(row.find('th').get_text()) for row in rows[1:]]
indexes
# %%
# lambda function to convert text to numbers 
to_num = lambda s: s[-1] == '%' and int(s[:-1]) or None

# %%
values = [to_num(remove_nl(value.get_text())) for row in rows[1:] for value in row.find_all('td')]
values 

# %%
stacked_values = list(zip(*[values[i::2] for i in range(len(columns))]))
stacked_values 
# %%
# exploding parameters
parameters = [100, 200, 300]
print(parameters, *parameters)
# %%
# dictionary comprehension
{ind: value for ind, value in zip(indexes, stacked_values)}
# %%
# pandas dataframes
df = pd.DataFrame(stacked_values, columns=columns, index = indexes)
df
# %%
df.dtypes
# %%
df.describe()
# %%
