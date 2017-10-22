import pandas as pd
pd.set_option('display.max_rows', 800)
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
observation_data = df[(~df['funded_year_month'].isin(['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12']))]
# I dropped user-item interaction data when the company had less than 2 investors,
# due to the the large number of users for which this applied.
# This sparse interaction data would be expected to hurt the performance of my recommendation model.
mask = observation_data.groupby('company_name')['investor_name'].count() >2
observation_data = observation_data[observation_data['company_name'].isin(mask[mask].index)]



# # Model 1: Only using interaction data, item-similarity model, Jaccard difference
interaction_data = observation_data[['company_name', 'investor_name']]
interaction_data.to_csv("interaction_data.csv")
sf = graphlab.SFrame.read_csv("interaction_data.csv")
m1 = graphlab.recommender.item_similarity_recommender.create(observation_data=sf, user_id = 'company_name', item_id = 'investor_name')
# m1.list_fields()
# m1.get_current_options()
# m1.get_similar_items()
# m1.evaluate(sf, exclude_known_for_precision_recall=False)
# m1.recommend(users=['23andMe'])
folds = KFold(sf, num_folds=5)
params = {'user_id':'company_name', 'item_id':'investor_name'}
job = cross_val_score(folds, graphlab.recommender.item_similarity_recommender.create, params)
job.get_results()



# # Model 2: Same as model 1, but with US city as item side data
mask = (observation_data[(observation_data['company_country_code'] == 'USA')].groupby('company_city').count() > 300)
big_cities_list = mask[(mask['company_name'] == True)]
cities = list(big_cities_list.index)
dummy_df = add_cities_dummies(df, cities)
dummy_df = dummy_df.drop(['company_permalink', 'company_city','company_category_list', 'company_country_code', 'company_state_code', 'company_region', 'investor_permalink', 'investor_country_code', 'investor_state_code', 'investor_region', 'investor_city', 'funding_round_permalink', 'funding_round_type', 'funding_round_code', 'funded_at', 'raised_amount_usd', 'funded_year', 'funded_year_month'], axis=1)
dummy_df.to_csv("interaction_data_2.csv")
dummy_df_user = dummy_df.drop('investor_name', axis=1)
dummy_df_user.to_csv("interaction_data_2_user.csv")

sf2 = graphlab.SFrame.read_csv("interaction_data_2.csv")
sf2_user  = graphlab.SFrame("interaction_data_2_user.csv")
m2 = graphlab.recommender.item_similarity_recommender.create(observation_data=sf2, user_id = 'company_name', item_id = 'investor_name', user_data=sf2_user)
folds = KFold(sf2, num_folds=5)
params = {'user_id':'company_name', 'item_id':'investor_name', 'user_data':sf2_user}
job = cross_val_score(folds, graphlab.recommender.item_similarity_recommender.create, params)
job.get_results()
