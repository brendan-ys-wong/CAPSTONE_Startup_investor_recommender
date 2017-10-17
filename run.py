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
df_influence

X = mrounds_hist(df_influence)
plt.plot(X)
plt.savefig('eigen_mrounds.png')
plt.show()
