import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from analysis_functions_v2 import *
import decimal
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

pd.set_option('display.max_rows', 300)
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df.head()

df = df_preprocessing(df)
seeded_companiesdf = df[(df['funding_round_type'] == 'seed') & (df['funded_year'] != '2014') & (df['funded_year'] != '2015')]
# There are 25K seeded companies not in 2014 or 2015. There 35K companies funded in 2014/2015.
seeded_companiesdf.head()


seeded_array = seeded_companiesdf['company_name'].unique()
#There are 10.8K unique seeded companies

mrounds_dict = mrounds_dict(df, seeded_array)
seeded_companiesdf['target'] = seeded_companiesdf['company_name'].apply(lambda x: mrounds_dict[x])
len(seeded_companiesdf)
sum(seeded_companiesdf['target'])
float(11215)/25171
#On Non-holdout data, the average rate of seeded companies moving on is 44.5% #BASELINE
#For holdout data, look at seeded companies in 2015 that that received seed in first 6 months of 2014.

shuffled_seeded_companiesdf = seeded_companiesdf.sample(frac=1)
len(shuffled_seeded_companiesdf)
sampled_shuffled_seeded = shuffled_seeded_companiesdf[0:20000]

G = node_and_edges(sampled_shuffled_seeded)
eig = nx.eigenvector_centrality_numpy(G)




X = seeded_companiesdf['raised_amount_usd'].as_matrix()
X = X.reshape(-1,1)
y = seeded_companiesdf['target'].as_matrix()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

logistic = LogisticRegression()
logistic.fit(X_train, y_train)
y_predict = logistic.predict(X_test)


print classification_report(y_test, y_predict)

logistic.score(X_test, y_test)
logistic.coef_








G = node_and_edges(df)
# There's 74.1K nodes. 44.6K nodes are companies, 30K nodes are investors. 670 are both.
len(G)
deg = nx.degree_centrality(G)
cent = nx.closeness_centrality(G)
len(deg)
deg
df_influence = influence_df(df, G)
len(df_influence)
