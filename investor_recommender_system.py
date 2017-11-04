import spacy
import pandas as pd
import numpy as np
from random import randint
import graphlab

# Functions
def cosine_sim(x):
    x_vec = nlp(unicode(x))
    return x_vec

def df_preprocessing(df):
    df = df.copy().fillna(value=0) # Used because 'Seed' funding types have naan for code column
    df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])
    df['funded_year_month'] = df['funded_year'] + "-" + df['funded_at'].apply(lambda x: x[5:7])
    df = df[(df['funding_round_type'] == 'seed') | (df['funding_round_type'] == 'venture')]

    interaction_data = df[['company_name', 'investor_name']]
    interaction_data.to_csv('path/to/interaction/data/file')
    return df

# Loading data and creating investor investment-count dataframe
df = pd.read_csv('Input/path/to/data/file')
df = df_preprocessing(df)
i_count = df.groupby('investor_name').count().sort_values('company_name', ascending=False)
i_count = i_count.reset_index()

# User Input
u_company = raw_input("Enter your company name: ")
u_type = raw_input("Recommendations: Enter 0 for seed investors or 1 for venture investors: ") 

# Recommendations based on company description
if u_type == '0':
    nlp = spacy.load('en_core_web_md')
    u_category = raw_input("Enter the industries your company belongs in. It's OK to enter multiple industries. (e.g. Games, Media, Mobile): ")
    df = df[(df['funding_round_type']=='seed')]
    cc = df[['company_name', 'company_category_list']]
    cc = cc.drop_duplicates()

    vec = nlp(unicode(u_category))
    cc['cosine_similarity'] = cc['company_category_list'].apply(lambda x: vec.similarity(cosine_sim(x)))
    cc = cc.sort_values(['cosine_similarity'], ascending=False)

    mask = (cc['cosine_similarity'] > 0.7)
    company_list = cc[mask]
    company_list = company_list.drop_duplicates()

    investor_set = set()
    for x in company_list['company_name']:
        investor_set.update(set(df[(df['company_name']==x)]['investor_name']))

    investor_set = list(investor_set)
    df_ret = pd.DataFrame(investor_set, columns=['investor_name'])
    df_ret = df_ret.merge(i_count,how='left')
    df_ret = df_ret.sort_values('company_name', ascending=False)

    ret_investors = list(df_ret['investor_name'].iloc[0:10])
    print ret_investors

# Recommendations based on investor list
if u_type == '1':
    u_investors = raw_input("Enter the full names of your current investors: (e.g. 500 Startups, Billie Jean): ")
    u_investors = u_investors.split(',')

    data_dict = {'X1':[], 'company_name': [], 'investor_name':[]}
    for investor in u_investors:
        data_dict['X1'].append(randint(200000, 201000))
        data_dict['company_name'].append(u_company)
        data_dict['investor_name'].append(investor)

    sf = graphlab.SFrame.read_csv('path/to/interaction/data/file')
    m1 = graphlab.recommender.item_similarity_recommender.create(observation_data=sf, user_id = 'company_name', item_id = 'investor_name')

    u_sf = graphlab.SFrame(data_dict)
    print m1.recommend(users=[u_company], new_observation_data=u_sf)
