#########
# data wrangling exercise
# created: May 20th, 2022
# author: minjoon

#%%
# all imports
import re  # regular expressions
import pickle
import socket
import operator
import time
import urllib
import numpy as np
from IPython.display import HTML
import pandas as pd

from bs4 import BeautifulSoup

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

sns.set_context("talk")
sns.set_style("white")

#%%
# read in user data
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']

users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols)
users.head()

# %%
# read in ratings
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']

ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols)
ratings.head()

# %%
# read movie data
m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']

movies = pd.read_csv('ml-100k/u.item', sep='|', names=m_cols, usecols=range(5))
movies.head()

# %%
users[users.age > 25].head()

# %%
# users aged 40 and male
male40s = users[(users.age == 40) & (users.sex == 'M')]
male40s

# %%
# users who are women and programmers 
women_prog = users[(users.sex == 'F') & (users.occupation == 'programmer')]
women_prog 
# %%
# mean age of women women programmers 
women_prog['age'].mean()

# %%
# finding diligent users
# split-apply-combine
ratings.head()

# %%
grouped_data = ratings['movie_id'].groupby(ratings['user_id'])
grouped_data.head()

# %%
# count and combine
ratings_per_user = grouped_data.count()
ratings_per_user.head(5) 

# %%
# group ratings by movie
movie_ratings_grouped = ratings.groupby('movie_id')
movie_ratings_grouped.head()

# %%
# get the average rating per movie
avg_ratings = movie_ratings_grouped['rating'].mean()
avg_ratings.head()
# %%
# get the movie titles with the highest average rating
# avg_ratings_sorted = avg_ratings.sort_values(ascending=False)
# movieids = avg_ratings_sorted.head().index 
# for id in movieids:
#     print(movies.loc[movies['movie_id'] == id, 'title'].item())

max_ratings = avg_ratings.max()
good_movie_ids = avg_ratings[avg_ratings == max_ratings].index 
good_movies = movies[movies.movie_id.isin(good_movie_ids)].title

print(good_movies)

# %%
# number of ratings per movie
ratings_per_movie = movie_ratings_grouped.count()
ratings_per_movie

# %%
# passing a function
# get the average rating per user 
grouped_data = ratings['rating'].groupby(ratings['user_id'])
average_ratings = grouped_data.mean()
average_ratings.head() 
# %%
occupations = users['sex'].groupby(users['occupation'])
occupations.head()

#%%
# male dominant occupations
male_dominant_occupations = occupations.apply(lambda f: sum(f == 'M') > sum(f == 'F'))
print("Male dominant occupations")
male_dominant_occupations

# %%
# web scrapping section

url = 'https://www.crummy.com/software/BeautifulSoup/'
source = urllib.request.urlopen(url).read()
source = source.decode('utf-8')


# %%
# is 'Alice' in source?
print('Alice' in source)
# %%
# count occurences of 'Soup'
print(source.count('Soup'))
# %%
# at what index occurs the substring 'Hall of Fame'?
phrase = source.find('Hall of Fame')
print(phrase)
print(source[phrase:phrase + len('Hall of Fame')])

# %%
# getting to BeautifulSoup
soup = BeautifulSoup(source)
# print(soup)
# print(soup.prettify())
# %%
# find all <a> tags
soup.findAll('a')
# %%
# 'find' finds tags, 'get' gets attributes i.e. href
first_tag = soup.find('a')
first_tag.get('href')
# %%
# get all links in the page
link_list = [l.get('href') for l in soup.findAll('a')]
link_list 

# %%
# filter all external links
external_links = []
for l in link_list:
    if l is not None and l[:4] == 'http':
        external_links.append(l)

external_links
# %%
# list comprehension version
[l for l in link_list if l is not None and l.startswith('http')]
# %%
# parsing the tree
s = """<!DOCTYPE html><html><head><title>This is a title</title></head><body><h3> Test </h3><p>Hello world!</p></body></html>"""

tree = BeautifulSoup(s)
# get html root node 
root_node = tree.html
# get head from root using contents
head = root_node.contents[0]
# get body from root
body = root_node.contents[1] 
# could also directly access body
tree.body 

# %%
# get h3 tag from body
print(body.contents[0])
# %%
# create a list of all hall of fame entries listed on the beautiful soup page
hof_list = soup.find('ul').findAll('li')
# %%
# skip the first entry
soup.find('ul').contents[1:] ## this seems to be the same as above. first entry is \n 
# %%
# reformat in to a list containing strings
# ... i already did it?? 
print(hof_list[2])

# %%
