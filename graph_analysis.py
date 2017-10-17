import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np

pd.set_option('display.max_rows', 1000)
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])

# Function for  nodal graph
def node_and_edges(df):
    """
    Function to create nodal graph object.

    Input: Dataframe
    Output: Graph object
    """
    company_list = list(df['company_name'].unique())
    investor_list = list(df['investor_name'].unique())
    edge_df = df[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')
    edge_list = []

    for i in range(len(edge_df)):
        edge_list.append((edge_df['investor_name'].values[i], edge_df['company_name'].values[i]))

    G = nx.Graph()
    G.add_nodes_from(investor_list, color='red', size=50)
    G.add_nodes_from(company_list, color='blue', size=50)
    G.add_edges_from(edge_list)
    return G

G = node_and_edges(df)


# Functions used in centrality calculations
def sorted_map(map):
    """
    Sort map object. For example, list of degrees from Graph object is return as a map.
    Input: map
    Output: sorted map
    """
    ms = sorted(map.iteritems(), key=lambda (k,v): (-v,k))
    return ms

def trim_degrees(g, degree=15):
    """
    Trim graph object based on minimum number of degrees per node.

    Input: graph object, and minimum number of degrees per node_list
    Output: trimmed graph object
    """
    g2 = g.copy()
    d = nx.degree(g2)
    for n in g2.nodes():
        if d[n] <= degree:
            g2.remove_node(n)
    return g2


# Degree Centrality
deg = nx.degree(G)
ds = sorted_map(deg)

# h=plt.hist(deg.values(), 1)
# plt.loglog(h[1][1:],h[0])
# plt.show()

# Reducing dataset to focus on high degrees nodes only
core = trim_degrees(G)

# Closeness Centrality
cent = nx.closeness_centrality(core)
cs = sorted_map(cent)

# h=plt.hist(cent.values(), bins=20)
# plt.loglog(h[1][1:],h[0])
# plt.show()

# Betweeness Centrality
bet = nx.betweenness_centrality(core)
bs = sorted_map(bet)

# Eigenvector Centrality
eig = nx.eigenvector_centrality_numpy(core)
es = sorted_map(eig)

# Most influential VC's
degree_names = [x[0] for x in ds[0:250]]
close_names = [x[0] for x in cs[0:250]]
bet_names = [x[0] for x in bs[0:250]]
eig_names = [x[0] for x in es[0:250]]

union_names = list(set(degree_names) | set(close_names) | set(bet_names))

influence_table = [[name, deg[name], cent[name], bet[name], eig[name]] for name in union_names]
influence_table = sorted(influence_table, key=lambda x: x[2], reverse=True)

# Histogram for 2009, most influential versus middle-of-the-pack
df_influence = pd.DataFrame(
    influence_table, columns=['company_name', 'degree_centrality',
    'closeness_centrality', 'betweenness_centrality', 'eigenvector_centrality'])
df_influence['influence_rank'] = [x/20 for x in df_influence.index]
company_list = list(df_2['company_name'].unique())
df_influence['type'] = [0 if x in company_list else 1 for x in df_influence['company_name']]

df_2 = df.copy().fillna(value=1)
df_company_rounds = df_2[['company_name', 'funding_round_type', 'funding_round_code']].groupby(
['company_name', 'funding_round_type', 'funding_round_code']).count()


company_rounds_list = [x for x in df_company_rounds.index]
freq_list = Counter(x[0] for x in company_rounds_list) # Company: # of Rounds

invest_dict = defaultdict(set)
for investor in df_influence['company_name']:
    invest_dict[investor] = set(df_2[(df_2['investor_name']==investor)]['company_name'])


def mrounds_rate(df, company_rounds_list, invest_dict):
    mrounds_rate = []
    for investor in df_influence['company_name']:
        mrounds_counter = 0
        company_set = invest_dict[investor]
        for company in company_set:
            nrounds = company_rounds_list[company]
            if nrounds > 1:
                mrounds_counter += 1
        try:
            mrounds_rate.append(float(mrounds_counter)/float(len(company_set)))
        except ZeroDivisionError:
            mrounds_rate.append(0)
    return mrounds_rate

mround_rate = mrounds_rate(df_2, freq_list, invest_dict)
df_influence['mrounds_rate'] = mround_rate
df_influence[(df_influence['type'] == 1)].reset_index()

def mrounds_hist(df):
    X = []
    for x in xrange(218):
        X.append(df.iloc[x]['mrounds_rate'])
    return X

df_investors_only = df_influence[(df_influence['type'] == 1)].reset_index()
X = mrounds_hist(df_investors_only)
plt.plot(X)
plt.show()
