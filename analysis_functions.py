import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np

def df_preprocessing(df):
    df = df.copy().fillna(value=1)
    df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])
    df = df[(df['funded_year'] != '2014') & (df['funded_year'] != '2015')  ]
    return df

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

# Functions used in centrality calculations
def sorted_map(G):
    """
    Sort map object. For example, list of degrees from Graph object is return as a map.
    Input: map
    Output: sorted map
    """
    ms = sorted(G.iteritems(), key=lambda (k,v): (-v,k))
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

def influence_df(df, G):
    """
    Calculates centrality metrics and produced influence dataframe.
    Inputs: dataframe, graph object
    Outputs: new dataframe
    """

    core = trim_degrees(G)
    deg = nx.degree(G) # Degree centrality
    ds = sorted_map(deg)
    cent = nx.closeness_centrality(core) # Closeness centrality
    cs = sorted_map(cent)
    bet = nx.betweenness_centrality(core) #Betweenness centrality
    bs = sorted_map(bet)
    eig = nx.eigenvector_centrality_numpy(core) #Eigenvector centrality
    es = sorted_map(eig)

    degree_names = [x[0] for x in ds[0:250]]
    close_names = [x[0] for x in cs[0:]]
    bet_names = [x[0] for x in bs[0:]]
    eig_names = [x[0] for x in es[0:]]

    union_names = list(set(degree_names) | set(close_names) | set(bet_names) | set(eig_names))
    influence_table = [[name, deg[name], cent[name], bet[name], eig[name]] for name in union_names]
    influence_table = sorted(influence_table, key=lambda x: x[4], reverse=True)

    df_influence = pd.DataFrame(
        influence_table, columns=['company_name', 'degree_centrality',
        'closeness_centrality', 'betweenness_centrality', 'eigenvector_centrality'])
    company_list = list(df['company_name'].unique())
    df_influence['type'] = [0 if x in company_list else 1 for x in df_influence['company_name']]
    df_influence = df_influence[(df_influence['type'] == 1)]
    df_influence['eigen_and_close'] = df_influence['closeness_centrality'] + df_influence['eigenvector_centrality']
    df_influence.sort_values('eigen_and_close', ascending=False, inplace=True)
    df_influence.reset_index(inplace=True)
    df_influence['influence_rank'] = [x/500 for x in df_influence.index]
    return df_influence

# Functions used in plotting mrounds_rate graphs
def add_mrounds_rate(df, df_influence):
    """
    Adds column to df_influence regarding the percentage of investments for each investors in the influence dataframe that have
    received multipl rounds of funding.
    Input: dataframe, influence dataframe
    Output: Amended influence dataframe
    """

    df_company_rounds = df[['company_name', 'funding_round_type', 'funding_round_code']].groupby(['company_name', 'funding_round_type', 'funding_round_code']).count()

    company_rounds_list = [x for x in df_company_rounds.index]
    freq_list = Counter(x[0] for x in company_rounds_list) # Company: # of Rounds

    invest_dict = defaultdict(set)
    for investor in df_influence['company_name']:
        invest_dict[investor] = set(df[(df['investor_name']==investor)]['company_name'])

    mrounds_rate = []
    for investor in df_influence['company_name']:
        mrounds_counter = 0
        company_set = invest_dict[investor]
        for company in company_set:
            nrounds = freq_list[company]
            if nrounds > 1:
                mrounds_counter += 1
        try:
            mrounds_rate.append(float(mrounds_counter)/float(len(company_set)))
        except ZeroDivisionError:
            mrounds_rate.append(0)

    df_influence['mrounds_rate'] = mrounds_rate

    return invest_dict, df_influence

def mrounds_hist(df):
    """
    Formula to produce a list of the rate of multiple rounds for each investor used
    for plotting purposes.

    Input: Data Frame
    Output: List of average rate of multiple rounds per investor
    """
    X = []
    for x in range(len(df)):
        X.append(df.iloc[x]['mrounds_rate'])
    return X

def weighted_avg(df):
    """
    Formula to produce a list of the average rate of multiple rounds for a group of investors used
    for plotting purposes.

    Input: Data Frame
    Output: List of average rate of multiple rounds per investor group
    """
    X = []
    avg_rate = df.groupby('influence_rank').mean()
    for x in range(len(avg_rate)):
        X.extend([avg_rate.iloc[x]['mrounds_rate']] * 500)
    return X

def mrounds_dict(df, company_list):
    """
    Create a dictionary with company name and a 1 if that company raise more
    than a seed round, and a 0 if it only raised a seed round.
    Input: Dataframe, list of Companies
    Output dictionary
    """
    df_company_rounds = df[['company_name', 'funding_round_type', 'funding_round_code']].groupby(['company_name', 'funding_round_type', 'funding_round_code']).count()
    g1 = pd.DataFrame({'count' : df_company_rounds.groupby( ['company_name','funding_round_type', 'funding_round_code'] ).size()}).reset_index()
    g2 = pd.DataFrame({'count' : g1.groupby( ['company_name','funding_round_type', 'funding_round_code'] ).size()}).reset_index()

    mrounds_dict = {}
    for company in company_list:
        if len(g2[(g2['company_name'] == company)]) > 1:
            mrounds_dict[company] = 1
        else:
            mrounds_dict[company] = 0
    return mrounds_dict

def add_eigen_close(key, influence_dict):
    """
    Add eigen_close column to an existing dataframe looked up by investor name.
    Input: dataframe
    Outpur: dataframe
    """

    try:
        return influence_dict['eigen_and_close'][key]
    except KeyError:
        return 0
