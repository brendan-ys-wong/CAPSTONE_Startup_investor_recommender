import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np

def df_preprocessing(df):
    df = df.copy().fillna(value=1) # Used because 'Seed' funding types have naan for code column
    df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])
    return df

def node_and_edges(df):
    """
    Function to create nodal graph object.

    Input: Dataframe
    Output: Graph object
    """
    company_list = set(df['company_name'])
    investor_list = set(df['investor_name'])
    edge_list = []

    for i in range(len(df)):
        edge_list.append((df['investor_name'].values[i], df['company_name'].values[i]))

    edge_list = set(edge_list)
    G = nx.Graph()
    G.add_nodes_from(investor_list, color='red', size=50)
    G.add_nodes_from(company_list, color='blue', size=50)
    G.add_edges_from(edge_list)
    return G

def influence_df(df, G):
    """
    Calculates centrality metrics and produced influence dataframe.
    Inputs: dataframe, graph object
    Outputs: new dataframe
    """

    deg = nx.degree_centrality(G) # Degree centrality
    cent = nx.closeness_centrality(G) # Closeness centrality
    bet = nx.betweenness_centrality(G) #Betweenness centrality
    eig = nx.eigenvector_centrality_numpy(G) #Eigenvector centrality

    degree_names = [x[0] for x in deg[0:]]
    close_names = [x[0] for x in cent[0:]]
    bet_names = [x[0] for x in bet[0:]]
    eig_names = [x[0] for x in eig[0:]]

    union_names = list(set(degree_names) | set(close_names) | set(bet_names) | set(eig_names))
    influence_table = [[name, deg[name], cent[name], bet[name], eig[name]] for name in union_names]

    df_influence = pd.DataFrame(
        influence_table, columns=['company_name', 'degree_centrality',
        'closeness_centrality', 'betweenness_centrality', 'eigenvector_centrality'])

    investor_list = set(df['investor_name'])
    df_influence['type'] = [1 if x in investor_list else 0 for x in df_influence['company_name']]
    df_influence = df_influence[(df_influence['type'] == 1)]
    df_influence['eigen_and_close'] = df_influence['closeness_centrality'] + df_influence['eigenvector_centrality']
    df_influence.sort_values('eigen_and_close', ascending=False, inplace=True)
    df_influence.reset_index(inplace=True)
    df_influence['influence_rank'] = [x/500 for x in df_influence.index]
    return df_influence

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
