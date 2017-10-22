import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np

def df_preprocessing(df):
    df = df.copy().fillna(value=0) # Used because 'Seed' funding types have naan for code column
    df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])
    df['funded_year_month'] = df['funded_year'] + "-" + df['funded_at'].apply(lambda x: x[5:7])
    df = df[(df['funding_round_type'] == 'seed') | (df['funding_round_type'] == 'venture')]
    return df

def add_cities_dummies(df, cities_list):
    for city in cities_list:
        df[city] = df['company_city'].apply(lambda x: 1 if x == city else 0)
    return df
