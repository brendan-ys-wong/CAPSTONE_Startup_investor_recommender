import spacy
import pandas as pd
import numpy as np

# Initialization & Set-up
nlp = spacy.load('en_core_web_md')

df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')
i_count = df.groupby('investor_name').count().sort_values('company_name', ascending=False)
i_count = i_count.reset_index()

# Functions
def cosine_sim(x):
    x_vec = nlp(unicode(x))
    return x_vec

# User Input Section
u_company = raw_input("Enter your company name: ")
u_type = raw_input("Enter 0 for seed investors or 1 for venture investors: ")

if u_type == '0':
    u_category = raw_input("Enter the industries your company belongs in. It's OK to enter multiple. (e.g. Games, Media): ")
    df = df[(df['funding_round_type']=='seed')]
    cc = df[['company_name', 'company_category_list']]
    cc = cc.drop_duplicates()


# Identify similar companies, then similar investors
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
