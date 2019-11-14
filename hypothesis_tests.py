"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject the null hypothesis" depending on the specified alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
import math
import numpy as np


def create_sample_dists(data, y_var, n_samples, sample_size):
    """Takes in either an np.array/list/pd Series, the number of samples we want to take, the size of each sample and creates a distribution of means, thus returning a normal distribution as Panda Series.
    data - the dataframe to be selected from;
    y_var - the numeric column name we're sampling from;
    n_samples - how many times should we sample from the population;
    sample_size - how large should each sample be"""
    sample_means = []
    for i in range(n_samples):
        sample = np.random.choice(data[y_var], size=sample_size, replace=True)
        sample_means.append(np.mean(sample))
    return pd.Series(sample_means)


def compare_pval_alpha(p_val, alpha):
    """Return a string status regarding whether the p value is greater than alpha or not
    p_val - the p-value obtained from a t-statistical test;
    alpha - our declared value of alpha for this hypothesis"""
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def Cohen_d(expr_sample, ctlr_sample):
    """Calculates the Cohen's d effect size for two groups; returns a float
    expr_sample - experiment sample
    ctlr_sample - control sample"""
    diff = expr_sample.mean() - ctlr_sample.mean()
    # Calculate the pooled threshold as shown earlier
    pooled_var = pooled_variance(expr_sample, ctlr_sample)
    
    # Calculate Cohen's d statistic
    d = diff / np.sqrt(pooled_var)
    
    return d


def welch_t(sample1, sample2):
    """Calculates the t-statistic using Welch's Test; returns a positive float"""
    numerator = np.mean(sample1) - np.mean(sample2)   
    denominator = np.sqrt(np.var(sample1)/len(sample1) + np.var(sample2)/len(sample2))
    return np.abs(numerator/denominator)    


def welch_dof(sample1,sample2):
    """Calculates the degrees of freedom for Welch's T-test"""
    s1 = np.var(sample1)
    s2 = np.var(sample2)
    n1 = len(sample1)
    n2 = len(sample2)
    
    num = (s1/n1 + s2/n2)**2
    denom = (s1/n1)**2/(n1-1) + (s2/n2)**2/(n2-1)
    return num/denom

def p_val(t_stat, df):
    return 1-stats.t.cdf(t_stat,df)



""" ________________________FUNCTIONS ABOVE__________________________________"""
""" _____________________HYPOTHESIS TESTS BELOW______________________________"""



def hypothesis_test_one(alpha = None, sample1, sample2, variable, num_samples, sample_size):
    """
    This hypothesis test should take in experimental (sample1) and control samples (sample2) and the variable column
    within those dfs which we wish to compare. Panda Dataframes/Series are expected. 
    This function will take num_samples amount of random samples (using np.random.choice) from the data, each of 
    size = sample size, and return a distribution of the sample means. Thus we gain a normal distribution. 
    The function will then calculate Welch's T-test, degrees of freedom, the p-value and determine if the null hypothesis
    can be rejected or not, and if it can, what is the effect size of the experimental sample. 
    sample1 - the experimental sample / post-intervention sample (pd.Dataframe / pd.Series)
    sample2 - the control sample (pd.Dataframe / pd.Series)
    alpha - your chosen alpha value (float)
    variable - which column in both samples is to be compared (string)
    num_samples - how many random samples should be taken from each of the data (int)
    sample_size - how large should each random sample be (int)
    
    returns the status (string)
    """
    # Get data for tests   data, y_var, n_samples, sample_size
    test_sample1 = create_sample_dists(data=sample1, y_var=variable, n_samples=num_samples, sample_size=sample_size)
    test_sample2 = create_sample_dists(data=sample2, y_var=variable, n_samples=num_samples, sample_size=sample_size)
    
    t_statistic = welch_t(test_sample1, test_sample2)
    
    dof = welch_dof(test_sample1, test_sample2)
    
    p_value = p_val(t_stat = t_statistic, df = dof)
    
    ###
    # Main chunk of code using t-tests or z-tests, effect size, power, etc
    ###

    # starter code for return statement and printed results
    status = compare_pval_alpha(p_value, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = Cohen_d(expr_sample=test_sample1, ctrl_sample=test_sample2)

    
       

    print(f'Based on the p value of {p_val} and our alpha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference between NONE')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

def hypothesis_test_two():
    pass

def hypothesis_test_three():
    

def hypothesis_test_four():
    pass
