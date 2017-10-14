import pandas as pd

def funding_count(df, round_type):
    """
    Input: Dataframe, name of funding_round_type
    Output: Integer, unique company funding round count
    """
    return (df[['company_name', 'funding_round_type']][(df['funding_round_type'] == round_type)]).groupby('company_name').count()

def funding_count_det(df, round_type):
    """
    Similar to funding_count function except it gives the detailed count by round type (e.g. A, B, C)
    Input: Dataframe, name of funding_round_type
    Output: Integer, count for each funding_round_code
    """
    funding_round_code_list = list(df[(df['funding_round_type'] == round_type)]['funding_round_code'].unique())

    for code in funding_round_code_list:
        print code, (
        df
        [['company_name', 'funding_round_type', 'funding_round_code']]
        [(df['funding_round_type'] == round_type)]
        [(df['funding_round_code'] == code)]
        ).groupby('company_name').count()

# # Companies with Series A
# comp_ser_a = df[['company_name', 'funding_round_type']][(df['funding_round_type'] == 'series-a')]
# # comp_ser_a.count
#
# # Target column representing future rounds
# df[['company_name', 'funding_round_type']].groupby(['company_name', 'funding_round_type']).count()

if __name__ == "__main__":
    df = pd.read_csv('/Users/brendanwong/galvanize/Capstone/crunchbase-data/investments.csv')

    # # Counts by funding_round_type
    # funding_rounds = list(df['funding_round_type'].unique())
    # for round_type in funding_rounds:
    #     print round_type, funding_count(df, round_type)

    funding_count_det(df, 'angel')
    # # Examining funding_round_code per funding_round_type
    # df[['company_name', 'funding_round_type', 'funding_round_code']].groupby(['company_name', 'funding_round_type', 'funding_round_code']).count()
    # df[(df['funding_round_type'] == 'seed')].head(100)
    # df[(df['funding_round_type'] == 'seed')][(df['funding_round_code']=='B')]
