# # Baseline
# - Seed & Venture Only
# - No 2H of 2015
# - 138K Total Transactions, 40K Seed transactions, 98K Venture transactions
import graphlab
from analysis_functions_similarity import *
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
df = df_preprocessing(df)
mask_d = (~df['funded_year_month'].isin(['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12']))
observation_data = df[mask_d]
len(observation_data)
seed = observation_data[(observation_data['funding_round_type'] == 'venture')]
seed = seed[(seed['company_country_code'] == 'FRA')]
len(seed)
seed_g = seed.groupby('investor_name').count().sort_values("company_name", ascending=False)

hits = sum(seed_g['company_name'].iloc[0:10])
hits
hits
seed_g['company_name'].iloc[0:10]



def country_count():
    countries = seed['investor_country_code'].unique()
    seed_c = seed.groupby('company_country_code').count().sort_values("company_name", ascending=False)
    seed_c


test_data = observation_data
len(test_data)
test_data.to_csv('/Users/brendanwong/galvanize/interaction_data/delete2_data.csv')
sf = graphlab.SFrame.read_csv('/Users/brendanwong/galvanize/interaction_data/delete2_data.csv')
train, test = graphlab.recommender.util.random_split_by_user(sf, user_id="company_name", item_id="investor_name", max_num_users=25000)
train_df = train.to_dataframe()
train_df = train_df[(train_df['funding_round_type'] == 'venture')]
train_list = train_df.groupby('investor_name').count().sort_values("company_name", ascending=False).reset_index()['investor_name'].iloc[0:40]
len(train_df)
train_list

test_df = test.to_dataframe()
test_df = test_df[(test_df['funding_round_type'] == 'seed')]

len(test_df)
sum(test_df['company_name'])
test_df = test_df.groupby('investor_name').count().sort_values("company_name", ascending=False).reset_index()

test = observation_data.groupby('investor_name').count()
test = test.sort_values('company_name', ascending=False).reset_index()
len(df)
type(test)

counter = 0
for name in train_list:
    x = test_df[(test_df['investor_name'] == name)]['company_name']
    counter += int(x)
counter
test_df[(test_df['investor_name'] == 'Accel')]['company_name']
