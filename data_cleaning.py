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

def format_time(data, date_col_name):
    """Takes in a dataframe, the column containing dates, and re-formats it to a datetime object,
    then creates two additional columns containing just Year and Month separately. """
    data[date_col_name] = pd.to_datetime(data[date_col_name])
    data['Year'] = data[date_col_name].dt.year
    data['Month'] = data[date_col_name].dt.month
    return data

def drop_null_values_and_cols(data, col_of_interest=[], col_to_drop=[]):
    """Takes in a dataframe, the columns you'd like to drop NaN values from, and any columns you'd like to drop. 
    data - your dataframe;
    col_of_interest - the column you want to clean of NaN values;
    col_to_drop - columns you'd like to drop
    """
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



def full_clean(input_data, date_column, columns_of_interest, column_to_drop, target_col, values_of_interest, output_file_name='clean_data_for_testing'):
    """
    This function runs the full clean on our data.
    input_data - data csv file name
    date_column - the column with dates / that we would like to format to DateTime objects
    columns_of_interest - the columns to clean of NaN values
    column_to_drop - columns we don't want any more
    target_col - the column we would like to filter by
    values_of_interest - the values we will use to filter our target_col by
    output_file_name - name for our csv file
    """
    dirty_data = pd.read_csv(input_data)

    cleaning_data1 = format_time(dirty_data, date_col_name=date_column)
    cleaning_data2 = drop_null_values_and_cols(cleaning_data1, col_of_interest=columns_of_interest, col_to_drop = column_to_drop)
    cleaned_data= create_test_sample(cleaning_data2, param_col = target_col, values = values_of_interest)
    
    cleaned_data.to_csv(f'./{output_file_name}.csv')
    
    return cleaned_data