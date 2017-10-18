import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from analysis_functions import *

pd.set_option('display.max_rows', 1000)
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df = df_preprocessing(df)

G = node_and_edges(df)

df_influence = influence_df(df, G)
df_influence = add_mrounds_rate(df, df_influence)
df_influence.head()

avg_rate = df_influence.groupby('influence_rank').mean()
avg_rate.head()
avg_rate.iloc[0]

df_influence['avg_mrounds_rate'] = df_influence.apply(lambda x: avg_rate.iloc[x]['mrounds_rate'] for x in df_influence['influence_rank'])


X = mrounds_hist(df_influence)

plt.plot(X)
plt.plot(mean['mrounds_rate'])
plt.savefig('eigen_and_closeness_mrounds.png')
plt.show()
