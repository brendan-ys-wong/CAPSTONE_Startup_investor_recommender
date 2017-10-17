import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from prettytable import PrettyTable

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


# Functions used in centrality calculations
def sorted_map(map):
    ms = sorted(map.iteritems(), key=lambda (k,v): (-v,k))
    return ms

def trim_degrees(g, degree=50):
    g2 = g.copy()
    d = nx.degree(g2)
    for n in g2.nodes():
        if d[n] <= degree:
            g2.remove_node(n)
    return g2


# Degree Centrality
deg = nx.degree(G)
ds = sorted_map(deg)
ds[0:10]

# h=plt.hist(deg.values(), 1)
# plt.loglog(h[1][1:],h[0])
# plt.show()

# Reducing dataset to focus on high degrees nodes only
core = trim_degrees(G)

# Closeness Centrality
cent = nx.closeness_centrality(core)
cs = sorted_map(cent)
cs[:10]

# h=plt.hist(cent.values(), bins=20)
# plt.loglog(h[1][1:],h[0])
# plt.show()

# Betweeness Centrality
bet = nx.betweenness_centrality(core)
bs = sorted_map(bet)
bs[0:10]

# Eigenvector Centrality
eig = nx.eigenvector_centrality(core)
es = sorted_map(eig)
es[0:10]

# Most influential VC's
degree_names = [x[0] for x in ds[0:10]]
close_names = [x[0] for x in cs[0:10]]
bet_names = [x[0] for x in bs[0:10]]
eig_names = [x[0] for x in es[0:10]]

union_names = list(set(degree_names) | set(close_names) | set(bet_names))

influence_table = [[name, deg[name], cent[name], bet[name], eig[name]] for name in union_names]
sorted(influence_table, key=lambda x: x[2])


# Histogram for 2009, most influential versus middle-of-the-pack

df_ht = df.copy()
