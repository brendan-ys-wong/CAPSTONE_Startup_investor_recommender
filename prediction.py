import pandas as pd


df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')

## Companies with seed
seeded_array = (df[(df['funding_round_type'] == 'seed')]['company_name'].unique())
seeded_array.shape

## Investors in seed
# beyond_seed = ['']
investors_array = (df[(df['funding_round_type'] == 'seed')]['investor_name'].unique())
investors_array.shape

## Sort investors by number of investments
investor_ct_df = (df[['investor_name', 'company_name']]).groupby('investor_name').count().sort_values('company_name', ascending=False)


# # Target column representing future rounds
# df[['company_name', 'funding_round_type']].groupby(['company_name', 'funding_round_type']).count()

def multiple_rounds_prob(df):
    """
    Inputs: Dataframe, integer representing investor size
    Bucket Sizes: {0:(0,10), 1:(11,50), 2:(51,200), 3:(201,400), 4:(401,700), 5:(700,1050)}

    Outputs: Average probability of securing multiple rounds
    """
    bucket_dict = {0:(0,10), 1:(11,50), 2:(51,200), 3:(201,400), 4:(401,700), 5:(700,1050)}
    company_dict =
    for key in bucket_dict.iterkeys():



if __name__ == "__main__":
    pass

    # # Examining funding_round_code per funding_round_type
    # df[['company_name', 'funding_round_type', 'funding_round_code']].groupby(['company_name', 'funding_round_type', 'funding_round_code']).count()
    # df[(df['funding_round_type'] == 'seed')].head(100)
    # df[(df['funding_round_type'] == 'seed')][(df['funding_round_code']=='B')]
