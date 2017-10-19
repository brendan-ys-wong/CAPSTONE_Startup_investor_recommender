import pandas as pd
import matplotlib # For EC2
matplotlib.use('Agg') # For EC2
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from analysis_functions import *

pd.set_option('display.max_rows', 1000)

# df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df = pd.read_csv('/home/ubuntu/Capstone/crunchbase-data/investments.csv') # For EC2

df = df_preprocessing(df)
G = node_and_edges(df)
df_influence = influence_df(df, G)
invest_dict, df_influence = add_mrounds_rate(df, df_influence)

# Plotting mrounds rate versus centrality metrics
# X = mrounds_hist(df_influence)
# X2 = weighted_avg(df_influence)
# fig, ax = plt.subplots()
# ax.set_ylabel("'%' investments raising post-seed")
# ax.set_xlabel('Investors ordered by eigenvalue & closeness ')
# plt.plot(X)
# plt.plot(X2)
# plt.savefig('weighted_eigenandclose_500.png')
# plt.show()

# Classification models

# new_influence_dict = df_influence[['company_name', 'eigen_and_close']]
# influence_dict = new_influence_dict.set_index(['company_name']).to_dict()
# influence_dict['eigen_and_close']['Accel']
#
# seeded_array = (df[(df['funding_round_type'] == 'seed')]['company_name'].unique())
# mrounds_dict = mrounds_dict(df, seeded_array)
#
# model_df = pd.DataFrame()
# model_df['company_name'] = seeded_array
# model_df['target'] = model_df['company_name'].apply(lambda x: mrounds_dict[x])
#
#
# centrality_lookupdf = df[(df['funding_round_type'] == 'seed')][['company_name', 'investor_name']]
# centrality_lookupdf['eigen_close'] = centrality_lookupdf['investor_name'].apply(lambda x: influence_dict['eigen_and_close'][x])
# centrality_lookupdf.head(20)
