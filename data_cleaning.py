"""
This module is for your data cleaning.
It should be repeatable.

## PRECLEANING
There should be a separate script recording how you transformed the json api calls into a dataframe and csv.

## SUPPORT FUNCTIONS
There can be an unlimited amount of support functions.
Each support function should have an informative name and return the partially cleaned bit of the dataset.
"""
import pandas as pd
import time
import scipy.stats as stats
import numpy as np

def format_time(data, date_col_name=''):
    data[date_col_name] = pd.to_datetime(data[date_col_name])
    data['Year'] = data[date_col_name].dt.year
    data['Month'] = data[date_col_name].dt.month
    return data

def drop_null_values_and_cols(data, col_of_interest=[], col_to_drop=[]):
"Takes in a dataframe, the columns you'd like to drop NaN values from, and any columns you'd like to drop"
    data = data.drop(columns=col_to_drop)
    for col in col_of_interest:
        data = data.loc[data[col].isna()==False]
    return data

def create_test_sample(data, param_col, values):
"""Takes in a dataframe and the columns you'd like to iterate over and the
particular value you want to filter by, 
e.g param_col = ['Year', 'Year'], values = [2017, 2009]"""
    test_dataframes=[]
    for i in range(len(values)):
        test_data=data.loc[data[param_col[i]] == values[i]]
        test_dataframes.append(test_data)
    return pd.concat(test_dataframes, axis=0)



def full_clean():
    """
    This is the one function called that will run all the support functions.
    Assumption: Your data will be saved in a data folder and named "dirty_data.csv"

    :return: cleaned dataset to be passed to hypothesis testing and visualization modules.
    """
    dirty_data = pd.read_csv("./data/dirty_data.csv")

    cleaning_data1 = support_function_one(dirty_data)
    cleaning_data2 = support_function_two(cleaning_data1)
    cleaned_data= support_function_three(cleaning_data2)
    cleaned_data.to_csv('./data/cleaned_for_testing.csv')
    
    return cleaned_data