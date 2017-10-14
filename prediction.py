import pandas as pd
from collections import defaultdict

def multiple_rounds_prob(df):
    """
    Inputs: Dataframe (cols: investor_name and seed investment count), integer representing investor size
    Bucket Sizes: {0:(0,10), 1:(11,50), 2:(51,200), 3:(201,400), 4:(401,700), 5:(700,1050)}

    Outputs: Average probability of securing multiple rounds
    """
    investor_df = (df[['investor_name', 'company_name']]).groupby('investor_name').count().sort_values('company_name', ascending=False)

    bucket_dict = {0:(0,10), 1:(11,50), 2:(51,200), 3:(201,400), 4:(401,700), 5:(700,1050)}

    for key in bucket_dict.iterkeys():
        company_list = []
        mrounds_list = []
        result_list = []

        low, high = bucket_dict[key]
        investor_list = (investor_df[(investor_df['company_name'] > low) & (investor_df['company_name'] < high)]).index.tolist()
        company_list = (df[(df['investor_name'].isin(investor_list))]['company_name']).unique().tolist()


        for company in company_list:
            if 'venture' in (df[(df['company_name'] == company)]['funding_round_type']).unique():
                mrounds_list.append(company)

        result_list.append(float(len(mrounds_list))/float(len(company_list)))

    return result_list

def v1_optimized_multiple_rounds_prob(df, low, high):
    """
    Inputs: Dataframe (cols: investor_name and seed investment count), integer representing investor size
    Bucket Sizes: {0:(0,10), 1:(11,50), 2:(51,200), 3:(201,400), 4:(401,700), 5:(700,1050)}

    Outputs: Average probability of securing multiple rounds
    """
    investor_df = (df[['investor_name', 'company_name']]).groupby('investor_name').count().sort_values('company_name', ascending=False)

    company_list = []
    mrounds_list = []
    result_list = []

    investor_list = (investor_df[(investor_df['company_name'] > low) & (investor_df['company_name'] < high)]).index.tolist()
    company_list = (df[(df['investor_name'].isin(investor_list))]['company_name']).unique().tolist()


    for company in company_list:
        if 'venture' in (df[(df['company_name'] == company)]['funding_round_type']).unique():
            mrounds_list.append(company)

    result_list.append(float(len(mrounds_list))/float(len(company_list)))

    return result_list

def v2_optimized_multiple_rounds_prob(df, low, high):
    """
    Inputs: Dataframe (cols: investor_name and seed investment count), integer representing investor size
    Bucket Sizes: {0:(0,10), 1:(11,50), 2:(51,200), 3:(201,400), 4:(401,700), 5:(700,1050)}

    Outputs: Average probability of securing multiple rounds
    """
    investor_df = (df[['investor_name', 'company_name']]).groupby('investor_name').count().sort_values('company_name', ascending=False)

    company_list = []
    mrounds_list = []
    result_list = []

    investor_list = (investor_df[(investor_df['company_name'] > low) & (investor_df['company_name'] < high)]).index.tolist()
    company_list = (df[(df['investor_name'].isin(investor_list))]['company_name']).unique().tolist()
    mrounds_list = (df['company_name'][((df['company_name'].isin(company_list)) & (df['funding_round_type']=='venture'))]).unique().tolist()

    return float(len(mrounds_list))/float(len(company_list))


if __name__ == "__main__":
    df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
    bucket_dict = {0:(0,10), 1:(11,50), 2:(51,200), 3:(201,400), 4:(401,700), 5:(700,1050)}
    for key in bucket_dict.iterkeys():
        low, high = bucket_dict[key]
        print v2_optimized_multiple_rounds_prob(df, low, high)


    ## Companies with seed
    # seeded_array = (df[(df['funding_round_type'] == 'seed')]['company_name'].unique())
    # seeded_array.shape

    ## Investors in seed
    # beyond_seed = ['']
    # investors_array = (df[(df['funding_round_type'] == 'seed')]['investor_name'].unique())
    # investors_array.shape

    ## Sort investors by number of investments
    # investor_ct_df = (df[['investor_name', 'company_name']]).groupby('investor_name').count().sort_values('company_name', ascending=False)
    # investor_ct_df.head(2)

    ## Target column representing future rounds
    # df[['company_name', 'funding_round_type']].groupby(['company_name', 'funding_round_type']).count()

    # # Examining funding_round_code per funding_round_type
    # df[['company_name', 'funding_round_type', 'funding_round_code']].groupby(['company_name', 'funding_round_type', 'funding_round_code']).count()
    # df[(df['funding_round_type'] == 'seed')].head(100)
    # df[(df['funding_round_type'] == 'seed')][(df['funding_round_code']=='B')]
