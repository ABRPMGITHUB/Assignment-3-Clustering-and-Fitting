# -*- coding: utf-8 -*-
"""Bhargavi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OxI19sfaGqFrvU_kuKBoUngO4iHXH9wr
"""

from google.colab import drive
drive.mount('/content/drive'

import pandas as pd
import numpy as np

def read_df(name):
    data_orig = pd.read_csv(name)
    data_1 = data_orig.drop(['Series Code', 'Country Code'],axis=1)
    #data_ag3=data_ag2.set_index("Country Name")
    data1 = data1[data_1['Series Name'] == 'CO2 emissions (kt)']
    data = pd.DataFrame.transpose(data_1)
    #data.reset_index(inplace=True)
    #data.rename(columns = {'index':'Year'}, inplace = True) 
    return data_orig,data

data_orig,data = read_df('/content/drive/MyDrive/57efe215-bce2-49a9-9dba-95fa6c91fe52_Data.csv')

ddata.head(10)

data.head()

data.head(10)
