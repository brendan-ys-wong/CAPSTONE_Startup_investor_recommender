import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])

# By year: Aggregated Node list (unique investors and companies)
company_list = list(df['company_name'].unique())
investor_list = list(df['investor_name'].unique())
node_list = company_list + investor_list

# By year: Edge list
edge_df = df[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')
edge_list = []
for i in range(len(edge_df)):
    edge_list.append((edge_df['investor_name'].values[i], edge_df['company_name'].values[i]))


G = nx.Graph()
G.add_nodes_from(investor_list, color='red', size=50)
G.add_nodes_from(company_list, color='blue', size=50)
G.add_edges_from(edge_list)


# Degree Centrality
deg = nx.degree(G)

min(deg.values())
max(deg.values())

def sorted_map(map):
    ms = sorted(map.iteritems(), key=lambda (k,v): (-v,k))
    return ms

ds = sorted_map(deg)
ds[0:99]

h=plt.hist(deg.values(), 100)
plt.loglog(h[1][1:],h[0])
plt.show()

def trim_degrees
