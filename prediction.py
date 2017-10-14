import pandas as pd

df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')

## Companies with seed
seeded_array = (df[(df['funding_round_type'] == 'seed')]['company_name'].unique())

## Investors post-seed
# beyond_seed = ['']
# investors_array = (df[(df['funding_round_type'] == 'seed')]['company_name'].unique())

#
# # Target column representing future rounds
# df[['company_name', 'funding_round_type']].groupby(['company_name', 'funding_round_type']).count()

if __name__ == "__main__":
    pass

    # # Examining funding_round_code per funding_round_type
    # df[['company_name', 'funding_round_type', 'funding_round_code']].groupby(['company_name', 'funding_round_type', 'funding_round_code']).count()
    # df[(df['funding_round_type'] == 'seed')].head(100)
    # df[(df['funding_round_type'] == 'seed')][(df['funding_round_code']=='B')]
