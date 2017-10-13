import pandas as pd

df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-october-2013/crunchbase-investments.csv')
print df.columns
df.head()

#Dataframe by year: Company, Funding Round Type, Amt Raised
df_2012 = df[(df['funded_year'] == 2012)]
df_2012 = df_2012[['company_name', 'funding_round_type', 'investor_name', 'raised_amount_usd']].sort_values(by='company_name')


df_2012_pairs = df_2012[['company_name', 'funding_round_type']]
df_2012_pairs.groupby(['company_name', 'funding_round_type']).count()
