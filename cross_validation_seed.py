import graphlab
import spacy
nlp = spacy.load('en_core_web_md')

df = pd.read_csv('/home/ubuntu/Capstone/crunchbase-data/investments.csv')
def df_preprocessing(df):
    df = df.copy().fillna(value=0) # Used because 'Seed' funding types have naan for code column
    df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])
    df['funded_year_month'] = df['funded_year'] + "-" + df['funded_at'].apply(lambda x: x[5:7])
    df = df[(df['funding_round_type'] == 'seed') | (df['funding_round_type'] == 'venture')]
    return df
df = df_preprocessing(df)
mask_d = (~df['funded_year_month'].isin(['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12']))
observation_data = df[mask_d]

i_count = df.groupby('investor_name').count().sort_values('company_name', ascending=False)
i_count = i_count.reset_index()

test_data = observation_data
test_data.to_csv('/home/ubuntu/Capstone/interaction_data/delete2_data.csv')
sf = graphlab.SFrame.read_csv('/home/ubuntu/Capstone/interaction_data/delete2_data.csv')
train, test = graphlab.recommender.util.random_split_by_user(sf, user_id="company_name", item_id="investor_name", max_num_users=25000)
train_df = train.to_dataframe()
train_df = train_df[(train_df['funding_round_type'] == 'seed')]

test_df = test.to_dataframe()
test_df = test_df[(test_df['funding_round_type'] == 'seed')]

test_df = test_df[['company_name', 'company_category_list']].drop_duplicates()
test_dict = {}

for company in test_df['company_name']:
    temp_df = train_df.copy()
    vec = nlp(unicode(company))
    temp_df['cosine_similarity'] = temp_df['company_category_list'].apply(lambda x: vec.similarity(cosine_sim(x)))
    temp_df = temp_df.sort_values(['cosine_similarity'], ascending=False)
    mask = (temp_df['cosine_similarity'] > 0.7)
    temp_df = temp_df[mask]

    investor_set = set()
    for x in temp_df['company_name']:
        investor_set.update(set(train_df[(train_df['company_name']==x)]['investor_name']))

    investor_set = list(investor_set)
    df_ret = pd.DataFrame(investor_set, columns=['investor_name'])
    df_ret = df_ret.merge(i_count,how='left')
    df_ret = df_ret.sort_values('company_name', ascending=False)

    ret_investors = list(df_ret['investor_name'].iloc[0:10])
    test_dict[company] = ret_investors
    break
