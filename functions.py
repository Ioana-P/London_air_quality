import os
from dotenv import load_dotenv
import requests as req
load_dotenv()
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

class APICaller:
    def __init__(self, base_url, token=None, ignore_token=False):
        self.token = os.getenv('TOKEN')
        if ignore_token==False:
            if len(self.token) == 0:
                raise ValueError('Missing API token!')
        self.base_url=base_url
        
    def retrieve_one(self,url_extension,location=None, date=None, date1=None):  
        if date1!=None:
            response = req.get(self.base_url+url_extension+f'{location}/StartDate={date}/EndDate={date1}/Json').json()
        elif (date!=None and date1==None):
            response = req.get(self.base_url+url_extension+f'{location}/Date={date}/Json').json()
        else:
            print(self.base_url+url_extension)
            response = req.get(self.base_url+url_extension).json()
        return response
    
    
    def retrieve_many(self,location_list, date_list, var, limit):
        data = []
        counter=0
        for location in location_list:
            for date in date_list:
                if counter==limit-1:
                    time.sleep(60)
                response = req.get(f'{self.url}/{key}/{location}/{date}/{var}').json()
                data.append(response)
                counter+=1
        data_df = pd.read_json(data)    
        return data_df
    
    
class Statistical_tester:
    def __init__(self, data0, data1=None):
        self.data0 = data0
        self.data1 = data1
        
    def sample_variance0(self):
        return np.sum([(x - np.mean(self.data0))**2 for x in self.data0])/(len(self.data0)-1)
    
    def sample_variance1(self):
        return np.sum([(x - np.mean(self.data1))**2 for x in self.data1])/(len(self.data1)-1)
    
    def describe(self, figsize):
        print('Our sample variance is ' + np.std(self.sample_variance0))
        print('Our sample mean is ' + np.mean(self.data0))
        if self.data1!=None:
            print('Our test sample variance is ' + np.std(self.sample_variance1))
            print('Our test sample mean is ' + np.mean(self.data1))
        return
    
    def pooled_variance(self):
    return ((len(self.data1)-1)*sample_variance(self.data1) + (len(sample2)-1)*sample_variance(sample2))/(len(sample1) + len(sample2) - 2)
    
    def twosample_tstatistic(self):
        return (np.mean(self.data1)-np.mean(self.data0))/np.sqrt(pooled_variance(expr,self.data0)*(1/len(self.data1) + 1/len(self.data0)))

    
    def welch_test(self):
        
        
        
        
    # Visualize t and p_value

    def visualize_t(self, t_stat, t_stat_type = 'one-tail', self.data0, self.data1, fig_size=(15,10) ):
        df = len(data1)-1
        # initialize a matplotlib "figure"
        fig = plt.figure(figsize=fig_size)
        ax = fig.gca()
        # generate points on the x axis between -4 and 4:
        xs = np.linspace(-5,5,1000)
        # use stats.t.pdf to get values on the probability density function for the t-distribution
        ys = stats.t.pdf(xs, df, 0, 1)
        ax.plot(xs, ys, linewidth=3, color='darkblue')
        if t_stat_type == 'one-tail':
            ax.axvline(x=t_stat, color='red', linestyle='--', lw=3,label='t_critical_value')
        elif t_stat_type == 'two-tail':
        # Draw two sided boundary for critical-t
            ax.axvline(x=+t_stat, color='red', linestyle='--', lw=3,label='t-statistic_lower_bound')
            ax.axvline(x=-t_stat, color='purple', linestyle='--', lw=3,label='t-statistic_upper_bound')
        ax.legend()
        plt.show()
        
        return 
    
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    