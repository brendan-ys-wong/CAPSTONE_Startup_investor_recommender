import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Oct 2013 dataset
# df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-october-2013/crunchbase-investments.csv')

# Dec 2015 dataset
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])
df.info()

# Set the year
df_year = df[(df['funded_year'] == '2015')]

# By year: Company, Funding Round Type, Investor Amt Raised
df_year[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')

# By year: Unique Company Rounds
df_year[['company_name', 'funding_round_type']].groupby(['company_name', 'funding_round_type']).count() #to get unique company rounds

By year: Unique Company list (Nodes)
company_list = list(df_year['company_name'].unique())
investor_list = list(df_year['investor_name'].unique())
node_list = company_list + investor_list

# By year: Weighted Edge list (e.g. (2, 3, {'weight': 3.1415}))
edge_df = df_year[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')
edge_list = []
for i in range(len(edge_df)):
    edge_list.append((edge_df['investor_name'].values[i], edge_df['company_name'].values[i]))


# Drawing node graph
G = nx.Graph()
G.add_nodes_from(investor_list, color='red', size=50)
G.add_nodes_from(company_list, color='blue', size=50)
G.add_edges_from(edge_list)
nx.draw(G)
plt.show()

de plot_multimode(4)
