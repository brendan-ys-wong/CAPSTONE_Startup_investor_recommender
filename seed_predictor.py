import spacy
import pandas as pd
import numpy as np
from random import randint
import graphlab
from analysis_functions_similarity import *

# Initialization & Set-up
df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
i_count = df.groupby('investor_name').count().sort_values('company_name', ascending=False)
i_count = i_count.reset_index()

# Functions
def cosine_sim(x):
    x_vec = nlp(unicode(x))
    return x_vec

# User Input Section
u_company = raw_input("Enter your company name: ")
u_type = raw_input("Recommendations: Enter 0 for seed investors or 1 for venture investors: ") # TODO: If something other than 0/1 entered

if u_type == '0':
    nlp = spacy.load('en_core_web_md')
    u_category = raw_input("Enter the industries your company belongs in. It's OK to enter multiple industries. (e.g. Games, Media, Mobile): ")
    df = df[(df['funding_round_type']=='seed')]
    cc = df[['company_name', 'company_category_list']]
    cc = cc.drop_duplicates()

# Identify similar companies, then similar investors
    vec = nlp(unicode(u_category))

    cc['cosine_similarity'] = cc['company_category_list'].apply(lambda x: vec.similarity(cosine_sim(x)))
    cc = cc.sort_values(['cosine_similarity'], ascending=False)

    mask = (cc['cosine_similarity'] > 0.7) # TODO: Edge case if there aren't 10 investors at this similarity level
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

if u_type == '1':
    u_investors = raw_input("Enter the full names of your current investors: (e.g. 500 Startups, Billie Jean): ")
    u_investors = u_investors.split(',')

    data_dict = {'X1':[], 'company_name': [], 'investor_name':[]}
    for investor in u_investors:
        data_dict['X1'].append(randint(200000, 201000))
        data_dict['company_name'].append(u_company)
        data_dict['investor_name'].append(investor)

    sf = graphlab.SFrame.read_csv('/Users/brendanwong/galvanize/interaction_data/interaction_data.csv')
    m1 = graphlab.recommender.item_similarity_recommender.create(observation_data=sf, user_id = 'company_name', item_id = 'investor_name')

    u_sf = graphlab.SFrame(data_dict)
    print m1.recommend(users=[u_company], new_observation_data=u_sf)
