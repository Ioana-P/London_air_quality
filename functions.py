import os
from dotenv import load_dotenv
import requests as req
load_dotenv()
import pandas

class APICaller:
    def __init__(self, url, token):
        self.url = url
        self.token = os.getenv('TOKEN')
        if len(self.token) == 0:
            raise ValueError('Missing API token!')
        
    def retrieve_one(location, date, var):
        key = self.token   
        response = req.get(f'{self.url}/{key}/{location}/{date}/{var}').json()
        return response
    
    
    def retrieve_many(location_list, date, var):
        data = []
        
        for location in location_list:
            response = req.get(f'{self.url}/{key}/{location}/{date}/{var}').json()
            data.append(response)
            
        return data
    