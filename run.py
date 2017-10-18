import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from analysis_functions import *

pd.set_option('display.max_rows', 1000)
# df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')

matplotlib.use('Agg')
df = pd.read_csv('/home/ubuntu/Capstone/crunchbase-data/investments.csv')

df = df_preprocessing(df)
df.head()

df_unique = df[['company_name', 'funding_round_type', 'funded_year']].groupby(['company_name', 'funding_round_type', 'funded_year']).count()
years = df['funded_year'].tolist()
year_counts = Counter(years)
df_counts = pd.DataFrame.from_dict(year_counts, orient='index')
df.plot(kind='bar')

plt.show()


G = node_and_edges(df)
df_influence = influence_df(df, G)
df_influence.head()

# Plotting mrounds rate versus centrality metrics
df_influence = add_mrounds_rate(df, df_influence)
X = mrounds_hist(df_influence)
X2 = weighted_avg(df_influence)


fig, ax = plt.subplots()
ax.set_ylabel("'%' investments raising post-seed")
ax.set_xlabel('Investors ordered by eigenvalue & closeness ')
plt.plot(X)
plt.plot(X2)
plt.savefig('weighted_eigenandclose_500.png')
plt.show()

# Plotting Eigen_and_close metric versus investor size
