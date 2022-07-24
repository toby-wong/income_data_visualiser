# import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import boto3

from os import listdir
from os.path import isfile, join

region_key = 'SA4 HH Weekly Income Counts.csv'
state_key = 'State HH Income Counts.csv'
bucket = 'income-data-counts'
s3 = boto3.resource('s3')
region_obj = s3.Object(bucket, region_key)

def get_csv_filenames():
    return [f for f in s3.Bucket(bucket).objects.all() if isfile(f.key)]

def df_to_csv(df):
    return df.to_csv()

def get_csv_data(filename):
    df = pd.read_csv('s3://income-data-counts/'+filename)
    return df

def multi_sort_csv(filename, queries):
    # queries = [{'column': 'column_name', 'query': 'query_string'}]
    df = pd.read_csv('s3://income-data-counts/'+filename)

    for query in queries:
        df = df[df[query['column']] == query['query']]

    return df

def get_regions():
    df = pd.read_csv('files/SA4 HH Weekly Income Counts.csv')
    return df['SA4 Region Name'].unique().tolist()

def get_states():
    df = pd.read_csv('files/State HH Income Counts.csv')
    return df['State'].unique().tolist()

def get_income_brackets(df):
    return df['Weekly Household Income'].unique().tolist()

def get_proportion(region):
    df1 = multi_sort_csv('SA4 HH Weekly Income Counts.csv', [{'column': 'SA4 Region Name', 'query': region}])
    r_count = df1['Count'].astype(int).sum()
    stateID = df1['State ID'].unique().tolist()[0]

    df2 = multi_sort_csv('State HH Income Counts.csv', [{'column': 'State ID', 'query': stateID}])
    state = df2['State'].unique().tolist()[0]
    s_count = df2['Count'].astype(int).sum()

    brackets = sorted(get_income_brackets(df1), key=lambda x: int(''.join(re.findall('[\d-]', x)).split('-')[0]))
    proportions = []

    for bracket in brackets:
        proportion = {'Bracket': bracket}
        df1_bracket = df1[df1['Weekly Household Income'] == bracket]
        proportion[region] = df1_bracket['Count'].astype(int).sum() / r_count
        df2_bracket = df2[df2['Weekly Household Income'] == bracket]
        proportion[state] = df2_bracket['Count'].astype(int).sum() / s_count
        proportions.append(proportion)

    return proportions

if __name__ == "__main__":
    # print(get_csv_filenames())
    # print(multi_sort_csv('State HH Income Counts.csv', [{'column': 'State', 'query': 'Tasmania'}, {'column': 'Household composition', 'query': 'Family households'}]))
    # print(get_regions())
    # print(get_states())
    p = get_proportion('Sydney - Eastern Suburbs')
    print([p[i]['New South Wales'] for i in range(len(p))])

    # p1 = list()
    # for x in range(len(p)):
    #     p1.append(p[x]['Sydney - Eastern Suburbs'])
    #     p1.append(p[x]['New South Wales'])

    # n=16
    # # r = np.arange(n)
    # width = 0.5

    # plt.bar(r, [p[i]['Sydney - Eastern Suburbs'] for i in range(len(p))], width=width, color='blue')
    # plt.bar(r+width, [p[i]['New South Wales'] for i in range(len(p))], width=width, color='red')
    # plt.xticks(r+width/2, [p[i]['Bracket'] for i in range(len(p))])
    # plt.title('Proportion of households by income bracket')
    # plt.legend(['Sydney - Eastern Suburbs', 'New South Wales'])
    # plt.show()

