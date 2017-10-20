import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from analysis_functions_similarity import *
import graphlab

import sys
reload(sys)
sys.setdefaultencoding('utf8')

pd.set_option('display.max_rows', 300)
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df = df_preprocessing(df)
df.head(20)

# Hold-out data is from the last 6 months of 2015
observation_data = df[(~df['funded_year_month'].isin(['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12']))]
observation_data.head()


# I dropped user-item interaction data when the company had less than 2 investors, due to the the large number of users for which this applied.
# This sparse interaction data would be expected to hurt the performance of my recommendation model.
mask = observation_data.groupby('company_name')['investor_name'].count() >2
mask[mask]
observation_data = observation_data[observation_data['company_name'].isin(mask[mask].index)]
observation_data.head()
len(observation_data['company_name'].unique())

# For investors as the item
interaction_data = observation_data[['company_name', 'investor_name']]
interaction_data.head(20)
interaction_data.to_csv("interaction_data.csv")

# For companies as the item
interaction_data = observation_data[['investor_name', 'company_name']]
interaction_data.head(20)
interaction_data.to_csv("interaction_data.csv")

sf = graphlab.SFrame.read_csv("interaction_data.csv")
m1 = graphlab.recommender.item_similarity_recommender.create(observation_data=sf, user_id = 'company_name', item_id = 'investor_name')
m1.list_fields()
m1.get_current_options()
m1.get_similar_users()
