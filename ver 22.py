# -*- coding: utf-8 -*-
"""Bhargavi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OxI19sfaGqFrvU_kuKBoUngO4iHXH9wr
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import sklearn.cluster as cluster
import sklearn.metrics as skmet
import matplotlib.pyplot as plt
import re

def read_df(name):
  """Reads in the data from the file. The series name, series code and country code columns are dropped. Selects only the data related to CO2 emissions (kt).
  Country name is set as index. The index is reset and the dataframe is transposed. Returns the original and transposed dataframes"""
  data_orig = pd.read_csv(name)
  data_1 = data_orig.drop(['Series Code', 'Country Code'], axis = 1)
  data_1 = data_1[data_1['Series Name'] == 'CO2 emissions (kt)'].drop(['Series Name'], axis = 1)
  data_1=data_1.set_index("Country Name")
  data_1.reset_index(inplace=True)
  #data.rename(columns = {'index':'Year'}, inplace = True) 
  data = pd.DataFrame.transpose(data_1)
  return data_orig, data

data_orig, data = read_df('/content/drive/MyDrive/57efe215-bce2-49a9-9dba-95fa6c91fe52_Data.csv')

df = pd.DataFrame.transpose(data)
print(df.head())

#shape of dataframe
print(df.shape)

#no missing values
df.isna().sum()

def clean_val(val):
  try:
    s = float(val)
  except:
    s = re.sub(r".*", np.nan, val)
  return s

def clean_features(dataframe):
  for col in dataframe.columns[1:]:
    dataframe[col] = [clean_val(val) for val in dataframe[col]]
  return dataframe

dataframe[col] = pd.Series([clean_val(val) for val in dataframe[col]])

df1.isna().sum()

df1

df[df['1990 [YR1990]'] == '2380']

round(df['1990 [YR1990]'])

def norm(array):
  """ Returns array normalised to [0,1]. Array can be a numpy array or a column of a dataframe"""
  min_val = np.min(array)
  max_val = np.max(array)
  scaled = (array-min_val) / (max_val-min_val)
  return scaled

def norm_df(df, first=0, last=None):
  """
  Returns all columns of the dataframe normalised to [0,1] with the exception of the first (containing the names)
  Calls function norm to do the normalisation of one column, but doing all in one function is also fine.
  First, last: columns from first to last (including) are normalised. Defaulted to all. None is the empty entry. The default corresponds
  """
  # iterate over all numerical columns
  for col in df.columns[first:last]: # excluding the first column
    df[col] = norm(df[col])
  return df

# extract columns for fitting
df_fit = df[["1990 [YR1990]", "2000 [YR2000]"]].copy()
# normalise dataframe and inspect result. Normalisation is done only on the extracted columns. .copy() prevents
# changes in df_fit to affect df. This make the plots with the original measurements possible
df_fit = norm_df(df_fit)
df_fit.describe()

df_fit

