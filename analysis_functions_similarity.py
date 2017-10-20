import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter, defaultdict
import numpy as np

def df_preprocessing(df):
    df = df.copy().fillna(value=1) # Used because 'Seed' funding types have naan for code column
    df['funded_year'] = df['funded_at'].apply(lambda x: x[0:4])
    df['funded_year_month'] = df['funded_year'] + "-" + df['funded_at'].apply(lambda x: x[5:7])
    return df
