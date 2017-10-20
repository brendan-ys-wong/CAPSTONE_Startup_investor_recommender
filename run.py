import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np
from analysis_functions import *
import decimal
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# Code for when running on AWS EC2
# import matplotlib
# matplotlib.use('Agg')
# df = pd.read_csv('/home/ubuntu/Capstone/crunchbase-data/investments.csv')

pd.set_option('display.max_rows', 300)
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')

# Initial set-up
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
eigen_dict = df_influence[['company_name', 'eigen_and_close']]
eigen_dict = eigen_dict.set_index(['company_name']).to_dict()

seeded_array = (df[(df['funding_round_type'] == 'seed')]['company_name'].unique())
mrounds_dict = mrounds_dict(df, seeded_array)

model_df = pd.DataFrame()
model_df['company_name'] = seeded_array
model_df['sum_eigen_close'] = model_df['company_name'].apply(lambda x: sum(centrality_lookupdf[(centrality_lookupdf['company_name'] == x)]['eigen_close']))
model_df['target'] = model_df['company_name'].apply(lambda x: mrounds_dict[x])


centrality_lookupdf = df[(df['funding_round_type'] == 'seed')][['company_name', 'investor_name']]
centrality_lookupdf['eigen_close'] = centrality_lookupdf['investor_name'].apply(lambda x: add_eigen_close(x, influence_dict))


X = model_df.drop(['company_name', 'target'], axis=1)
y = model_df['target'].as_matrix()
len(y)
sum(y)
float(2420)/10753
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

logistic = LogisticRegression()
logistic.fit(X_train, y_train)
y_predict = logistic.predict(X_test)
logistic.score(X_test, y_test)
logistic.coef_

len(y_predict)
sum(y_predict)
float(19)/1613


print classification_report(y_test, y_predict)


cross_val_score(logistic, X, y, cv=10)
