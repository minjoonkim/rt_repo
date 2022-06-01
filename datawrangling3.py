#########
# data wrangling exercise #3
# created: May 26th, 2022
# author: minjoon

#%%
# all imports
import numpy as np 
import scipy as sp 
import matplotlib as mpl
import matplotlib.cm as cm 
import matplotlib.pyplot as plt 
# %matplotlib inline 

import pandas as pd
import time 
import seaborn as sns 
sns.set_style("whitegrid")
sns.set_context("poster")

from sqlite3 import dbapi2 as sq3
import os 

#%% 

ourschema = """
DROP TABLE IF EXISTS "candidates";
DROP TABLE IF EXISTS "contributors";
CREATE TABLE "candidates" (
    "id" INTEGER PRIMARY KEY  NOT NULL ,
    "first_name" VARCHAR,
    "last_name" VARCHAR,
    "middle_name" VARCHAR,
    "party" VARCHAR NOT NULL
);
CREATE TABLE "contributors" (
    "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
    "last_name" VARCHAR,
    "first_name" VARCHAR,
    "middle_name" VARCHAR,
    "street_1" VARCHAR,
    "street_2" VARCHAR,
    "city" VARCHAR,
    "state" VARCHAR,
    "zip" VARCHAR,
    "amount" INTEGER,
    "date" DATETIME,
    "candidate_id" INTEGER NOT NULL,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);
"""

# %%
PATHSTART="."
def get_db(dbfile):
    sqlite_db = sq3.connect(os.path.join(PATHSTART, dbfile))
    return sqlite_db

def init_db(dbfile, schema):
    """creates the database tables"""
    db = get_db(dbfile)
    db.cursor().executescript(schema)
    db.commit()
    return db

def make_query(sel):
    c = db.cursor().execute(sel)
    return c.fetchall()


cont_cols = [e[1] for e in make_query("PRAGMA table_info(contributors);")]

def make_frame(list_of_tuples, legend=cont_cols):
    framelist = []
    for i, cname in enumerate(legend):
        framelist.append((cname, [e[i] for e in list_of_tuples]))
    return pd.DataFrame.from_items(framelist)

# %%
dfcand = pd.read_csv("./candidates.txt", sep='|')
dfcand
# %%
dfcwci = pd.read_csv("./contributors_with_candidate_id.txt", sep='|')
dfcwci.head()
# %%
del dfcwci['id']
dfcwci.head()

# %%
# initialize database
db = init_db("cancont.db", ourschema)
# %%
# populating the db with pandas
dfcand.to_sql("candidates", db, if_exists="append", index=False)
dfcwci.to_sql("contributors", db, if_exists="append", index=False)
# %%
sel = """SELECT * FROM candidates;"""
c = db.cursor().execute(sel)
# %%
c.fetchall()
# %%
rem = """DELETE FROM candidates;"""
c = db.cursor().execute(rem)
db.commit()
# %%
c.fetchall()
# %%
# Single Table Verbs
# core data manipulation commands: these are universal across all systems
dfcwci.head()
# %%
# querying
dfcwci.query("state == 'VA' & amount < 400")
# %%
# compared with pandas
dfcwci[(dfcwci.state == 'VA') & (dfcwci.amount < 400)]
# %%
# SQL
out = make_query("SELECT * FROM contributors WHERE state='VA' AND amount < 400;")
# make_frame(out).head(10)
# %%
out = make_query("SELECT * FROM contributors WHERE state IN ('VA','WA');")
# make_frame(out).head(10)
# %%
dfcwci[dfcwci.state.isin(['VA', 'WA'])].head(10)

# %%
dfcwci.query("10 <= amount <= 50 ").head(10)
# %%
# pandas & sql 
pd.read_sql("SELECT * FROM candidates WHERE party= 'D';", db)
# %%
