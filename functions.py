import os
from dotenv import load_dotenv
import requests as req
load_dotenv()
import time
import pandas as pd
import numpy as np


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
    
    

 