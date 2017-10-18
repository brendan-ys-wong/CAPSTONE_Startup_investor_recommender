import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def funding_count(df, round_type):
    """
    Input: Dataframe, name of funding_round_type
    Output: Integer, unique company funding round count
    """
    return (df[['company_name', 'funding_round_type']][(df['funding_round_type'] == round_type)]).groupby('company_name').count()

def funding_count_det(df, round_type):
    """
    Similar to funding_count function except it gives the detailed count by round type (e.g. A, B, C)
    Input: Dataframe, name of funding_round_type
    Output: Integer, count for each funding_round_code
    """
    funding_round_code_list = list(df[(df['funding_round_type'] == round_type)]['funding_round_code'].unique())

    for code in funding_round_code_list:
        print code, (
        df
        [['company_name', 'funding_round_type', 'funding_round_code']]
        [(df['funding_round_type'] == round_type)]
        [(df['funding_round_code'] == code)]
        ).groupby('company_name').count()

if __name__ == "__main__":
    ### Oct 2013 dataset
    # df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-october-2013/crunchbase-investments.csv')

    ## Dec 2015 dataset
    df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
    df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])

    ## By year statistics:
    # Set the year:
    df_year = df[(df['funded_year'] == '2015')]

    ## By year: Company, Funding Round Type, Investor Amt Raised
    # df_year[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')

    ## By year: Unique Company Rounds
    df_year[['company_name', 'funding_round_type']].groupby(['company_name', 'funding_round_type']).count()

    ## By year: Aggregated Node list (unique investors and companies)
    # company_list = list(df_year['company_name'].unique())
    # investor_list = list(df_year['investor_name'].unique())
    # node_list = company_list + investor_list

    ## By year: Edge list
    # edge_df = df_year[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')
    # edge_list = []
    # for i in range(len(edge_df)):
        # edge_list.append((edge_df['investor_name'].values[i], edge_df['company_name'].values[i]))

    ### Drawing node graph
    # G = nx.Graph()
    # G.add_nodes_from(investor_list, color='red', size=50)
    # G.add_nodes_from(company_list, color='blue', size=50)
    # G.add_edges_from(edge_list)
    # nx.draw(G)
    # plt.show()

    ### By funding type:
    ## Counts by funding type
    # funding_rounds = list(df['funding_round_type'].unique())
    # for round_type in funding_rounds:
    #     print round_type, funding_count(df, round_type)

    ## Funding round code by funding type
    # funding_count_det(df, 'angel')
