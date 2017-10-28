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

df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df = df_preprocessing(df)
df.head()
mask_d = (~df['funded_year_month'].isin(['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12']))
observation_data = df[mask_d]
# observation_data = observation_data[(observation_data['funding_round_type'] == 'venture')]
holdout_data = df[(df['funded_year_month'].isin(['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12']))]

holdout_data = holdout_data[(holdout_data['funding_round_type'] == 'venture')]
train = observation_data[['company_name', 'investor_name']]
test = holdout_data[['company_name', 'investor_name']]
train.to_csv('/Users/brendanwong/galvanize/interaction_data/interaction_data_final.csv')
test.to_csv('/Users/brendanwong/galvanize/interaction_data/test_data_final.csv')
sf = graphlab.SFrame.read_csv('/Users/brendanwong/galvanize/interaction_data/interaction_data_final.csv')
sf_test = graphlab.SFrame.read_csv('/Users/brendanwong/galvanize/interaction_data/test_data_final.csv')
m2 = graphlab.recommender.item_similarity_recommender.create(observation_data=sf, user_id = 'company_name', item_id = 'investor_name', similarity_type='pearson')
eval_2 = m2.evaluate(sf_test, cutoffs=[10])
eval_2

m2.recommend(['Amino'])
m2.recommend(['Yozio'], k=20).print_rows(20)

m2.recommend().print_rows(200)
# observation_data['company_name'].unique()
# # holdout_data[(holdout_data['company_name'] == '4moms')]
# observation_data[(observation_data['company_name'] == 'Yozio')]
# # hg = holdout_data.groupby('investor_name').count()
# hg = hg.sort_values('company_name', ascending=False)
# hg.head(50)
# len(hg)
# m2.recommend(['Affinio'])
# holdout_data['company_name']
