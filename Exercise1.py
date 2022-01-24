# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 16:07:39 2022

@author: vnatarajan
"""


import requests
import pandas as pd
import numpy as np
import json

def extractRawData(inputList,URL):
    raw_data = pd.DataFrame([])
    for value in inputList:
        response = requests.get(URL + str(value))
        if response.ok:            
            responseData = json.loads(response.text)
            temp_df = pd.json_normalize(responseData['data'])            
            raw_data = raw_data.append(temp_df,ignore_index=True,sort=False)
        else:            
            new_row = {'id':value}
            raw_data = raw_data.append(new_row,ignore_index=True,sort=False)
    return raw_data
  

def replaceSeriesValue(series,oldValue,newValue):
    series = series.replace(to_replace = oldValue, value = newValue)
    return series
    

def transformData(df):
    df['year'] = replaceSeriesValue(df['year'],2010,2099)
    return df
    

inputList = [1,2,3,4,5,6,7,8,9,10,11,500,501]
URL = 'https://reqres.in/api/products/'
df = extractRawData(inputList,URL)
df = transformData(df)
print ('Median Year of Product is ' + str(int(df['year'].median())))
