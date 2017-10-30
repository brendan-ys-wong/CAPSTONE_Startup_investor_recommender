import pandas as pd
pd.set_option('display.max_rows', 800)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 200)
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from analysis_functions_similarity import *
import graphlab
from graphlab.toolkits.cross_validation import cross_val_score, KFold


import sys
reload(sys)
sys.setdefaultencoding('utf8')

# # Data ETL Pipeline
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df = df_preprocessing(df)
# Hold-out data is from the last 6 months of 2015
mask_d = (~df['funded_year_month'].isin(['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12']))
observation_data = df[mask_d]
# I dropped user-item interaction data for investors that had less than 50 investments,
# due to the the large number of users for which this applied.
# This sparse interaction data would be expected to hurt the performance of my recommendation model.
mask_i = (observation_data.groupby('investor_name')['company_name'].apply(lambda g: len(g) >50))
observation_data_large = observation_data[(observation_data['investor_name'].isin(mask_i[mask_i].index))]
len(observation_data_large)

# # Model 1: Only using interaction data, item-similarity model, Jaccard difference, 50+ investors
interaction_data = observation_data_large[['company_name', 'investor_name']]
interaction_data.to_csv('/Users/brendanwong/galvanize/interaction_data/interaction_data.csv')
sf = graphlab.SFrame.read_csv('/Users/brendanwong/galvanize/interaction_data/interaction_data.csv')
train, test = graphlab.recommender.util.random_split_by_user(sf, user_id="company_name", item_id="investor_name", max_num_users=25000)
m1 = graphlab.recommender.item_similarity_recommender.create(observation_data=train, user_id = 'company_name', item_id = 'investor_name')
eval_1 = m1.evaluate(test2, cutoffs=[40])
eval_1


# # Model 2: Same as model 1, but using all investors
interaction_data2 = observation_data[['company_name', 'investor_name']]
interaction_data2.to_csv('/Users/brendanwong/galvanize/interaction_data/interaction_data2.csv')
sf2 = graphlab.SFrame.read_csv('/Users/brendanwong/galvanize/interaction_data/interaction_data2.csv')
train2, test2 = graphlab.recommender.util.random_split_by_user(sf2, user_id="company_name", item_id="investor_name", max_num_users=25000)
m2 = graphlab.recommender.item_similarity_recommender.create(observation_data=train2, user_id = 'company_name', item_id = 'investor_name')
eval_2 = m2.evaluate(test2, cutoffs=[30])
eval_2
test2['company_name'].unique()
m2.recommend(['Beijing Weiying Technology'])

a = observation_data.groupby('investor_name').count()
a = a.sort_values('company_name', ascending=False)
a

# # Cross Validation
# folds = KFold(sf, num_folds=5)
# params = {'user_id':'company_name', 'item_id':'investor_name'}
# job = cross_val_score(folds, graphlab.recommender.item_similarity_recommender.create, params)
# job.get_results()
