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
from statsmodels.stats.power import TTestIndPower, TTestPower
import seaborn as sns
import matplotlib.pyplot as plt


def create_sample_dists(data, y_var, n_samples, sample_size):
    """Takes in either an np.array/list/pd Series, the number of samples we want to take, the size of each sample and creates a distribution of means, thus returning a normal distribution as Panda Series.
    data - the dataframe to be selected from;
    y_var - the numeric column name we're sampling from;
    n_samples - how many times should we sample from the population;
    sample_size - how large should each sample be"""
    sample_means = []
    np.random.seed(12345)
    for i in range(n_samples):
        sample = np.random.choice(data[y_var], size=sample_size, replace=True)
        sample_means.append(np.mean(sample))
    return pd.Series(sample_means)


def compare_pval_alpha(p_val, alpha):
    """Return a string status regarding whether the p value is greater than alpha or not
    p_val - the p-value obtained from a t-statistical test;
    alpha - our declared value of alpha for this hypothesis"""
    status = ''
    if p_val >= alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status

def pool_var(sample1, sample2):
    # Calculates the pooled variances for two samples
    return ((len(sample1)-1)*np.var(sample1) + (len(sample2)-1)*np.var(sample2))/(len(sample1) + len(sample2) - 2)




def welch_t(sample1, sample2):
    """Calculates the t-statistic using Welch's Test; returns a positive float"""
    numerator = np.mean(sample1) - np.mean(sample2)   
    denominator = np.sqrt(np.var(sample1)/len(sample1) + np.var(sample2)/len(sample2))
    return np.abs(numerator/denominator)    

def Cohen_d(expr_sample, ctrl_sample):
    diff = expr_sample.mean() - ctrl_sample.mean()
    pooled_variance = pool_var(expr_sample, ctrl_sample)
    # Calculate Cohen's d statistic
    d = diff / np.sqrt(pooled_variance)
    
    return d

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
    """Calculates the p value by calculating the complement of the cumulative density t-function using our
    degrees of freedom"""
    return 1-stats.t.cdf(t_stat,df)


def plot_dists(sample_list, label_list, colours_list):
    
    x = sns.distplot(sample_list[0],color=colours_list[0], bins=10, label=label_list[0])
    y = sns.distplot(sample_list[1], color=colours_list[1], bins=10, label=label_list[1])
    lines = plt.vlines([np.mean(sample_list[0]),np.mean(sample_list[1])],ymin=0, ymax=0.3, label='Mean values')
    return x,y,lines,plt.legend()


def visualize_one_side_t(t_stat, n_control, n_experimental, df, title):
    # initialize a matplotlib "figure"
    fig = plt.figure(figsize=(15,10))
    ax = fig.gca()
    # generate points on the x axis between -4 and 4:
    xs = np.linspace(-4,4,200)
    # use stats.t.pdf to get values on the probability density function for the t-distribution
    ys = stats.t.pdf(xs, df, 0, 1)
    ax.plot(xs, ys, linewidth=3, color='darkblue')

    # Draw one sided boundary for critical-t
    ax.axvline(x=+t_stat, color='red', linestyle='--', lw=3,label='t-statistic')
    ax.legend()
    plt.show()
    return 




""" ________________________FUNCTIONS ABOVE__________________________________"""
""" _____________________HYPOTHESIS TESTS BELOW______________________________"""



def hypothesis_test_one(sample1, sample2, 
                        variable, num_samples, 
                        sample_size,
                        sample1_label, sample2_label,
                        sample1_colour, sample2_colour,
                        alpha = None):
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
    
    test_samples = [test_sample1, test_sample2]
    test_samples_labels = [sample1_label, sample2_label]
    test_samples_colours = [sample1_colour, sample2_colour]
    
    
    plot_dists(test_samples, test_samples_labels, test_samples_colours)
    
    
    t_statistic = welch_t(test_sample1, test_sample2)
    
    dof = welch_dof(test_sample1, test_sample2)
    
    p_value = p_val(t_stat = t_statistic, df = dof)
    
    ###
    # Main chunk of code using t-tests or z-tests, effect size, power, etc
    ###
    power_analysis = TTestIndPower()
    
    # starter code for return statement and printed results
    status = compare_pval_alpha(p_value, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = Cohen_d(expr_sample=test_sample1, ctrl_sample=test_sample2)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=len(sample1), alpha=alpha)

    
    
    
    # Here we generate our final statement on whether our null hypothesis can be rejected or not and what 
    # our effect size is, if the H0 is rejected.

    print(f'Based on the p value of {p_value} and our alpha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference between our samples ')

    if assertion == 'can':
        print(f"with an effect size, Cohen's d, of {str(round(coh_d,3))} and power of {power}.")
    else:
        print(".")

    return (status, assertion, coh_d, t_statistic, dof)



"""___________________________________________________________________________________________"""


def hypothesis_test_two(sample1, sample2, 
                        sample1_label, sample2_label,
                        sample1_colour, sample2_colour,
                        variable, num_samples, 
                        sample_size, 
                        first_factor,
                        other_sample1, other_sample2, 
                        other_sample1_label, other_sample2_label,
                        other_sample1_colour, other_sample2_colour,
                        second_factor,
                        alpha = None, var_of_interest):
    
    """
    This hypothesis test will conduct the first hypothesis test for two pairs of samples (designated as sample1, sample2 
    and other_sample1, other_sample2. It then prints the status for both signifance tests and then returns the statement with 
    a comparison of the two effect sizes.
    first_factor - name of the factor whose effect you're testing for; first one to appear in statement
    second_factor - name of the second factor; second to appear in statement. """
    
    # running hypothesis tests number 1 on each pair of data, setting variables for the cohen's d
    # and for the assertion regarding the null hypotheses. 
    first_test = hypothesis_test_one(sample1, sample2,
                                     variable, num_samples, 
                                     sample_size, 
                                     sample1_label, sample2_label,
                                     sample1_colour, sample2_colour,
                                     alpha = alpha)
    
    
    assertion = first_test[1]
    if assertion=='can':
        assertion1=True
        coh_d1 = first_test[2]
    
    
 
    second_test = hypothesis_test_one(other_sample1, other_sample2, 
                                      variable, num_samples, 
                                      sample_size, 
                                      other_sample1_label, other_sample2_label,
                                      other_sample1_colour, other_sample2_colour,
                                      alpha = alpha)
    
    
    assertion = second_test[1]
    if assertion=='can':
        assertion2=True
        coh_d2 = second_test[2]
    
    # assuming both null hypotheses are rejected, the cohen's d is compared for the two pairs 
    # and we have a statement printed that compares the two, plus 
    
    
    if abs(coh_d1)>abs(coh_d2):
        difference='greater'
    else:
        difference='less'
    
    print(first_test[0],'\n')
    print(second_test[0],'\n')
    
    if first_factor==None:
        first_factor='first_factor'
        
    if second_factor==None:
        second_factor='second_factor'
    
    
    if assertion1 and assertion2:
        statement = f"The effect of {first_factor} on the levels of {var_of_interest} was {abs(coh_d1/coh_d2)} times {difference} than the effect of {second_factor}."
        
    return statement
    
