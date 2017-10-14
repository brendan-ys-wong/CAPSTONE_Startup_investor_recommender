import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-october-2013/crunchbase-investments.csv')
print df.columns
df.head()

# Set the year
df_year = df[(df['funded_year'] == 2004)]

# By year: Company, Funding Round Type, Investor Amt Raised
df_year[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')

# By year: Unique Company Rounds
df_year[['company_name', 'funding_round_type']].groupby(['company_name', 'funding_round_type']).count() #to get unique company rounds

# By year: Unique Company list (Nodes)
company_list = list(df_year['company_name'].unique())
investor_list = list(df_year['investor_name'].unique())
node_list = company_list + investor_list

# By year: Weighted Edge list (e.g. (2, 3, {'weight': 3.1415}))
edge_df = df_year[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')
edge_df['edge_list'] = (edge_df['investor_name'] + ', ' + edge_df['company_name'])


edge_list = []
for i in range(len(summary)):
    edge_list.append(tuple(edge_df['edge_list'].iloc[i:i+1]))
