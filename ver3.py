# -*- coding: utf-8 -*-
"""Bhargavi ADS 1.ipynb

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
    s = int(val)
  except:
    s = re.sub(r".*", '0', val)
  return s

print(df.head())

df['1990 [YR1990]'] = [int(clean_val(val)) for val in df['1990 [YR1990]']]
df['2000 [YR2000]'] = [int(clean_val(val)) for val in df['2000 [YR2000]']]
df['2012 [YR2012]'] = [int(clean_val(val)) for val in df['2012 [YR2012]']]
df['2013 [YR2013]'] = [int(clean_val(val)) for val in df['2013 [YR2013]']]
df['2014 [YR2014]'] = [int(clean_val(val)) for val in df['2014 [YR2014]']]
df['2015 [YR2015]'] = [int(clean_val(val)) for val in df['2015 [YR2015]']]
df['2016 [YR2016]'] = [int(clean_val(val)) for val in df['2016 [YR2016]']]
df['2017 [YR2017]'] = [int(clean_val(val)) for val in df['2017 [YR2017]']]
df['2018 [YR2018]'] = [int(clean_val(val)) for val in df['2018 [YR2018]']]
df['2019 [YR2019]'] = [int(clean_val(val)) for val in df['2019 [YR2019]']]
df['2020 [YR2020]'] = [int(clean_val(val)) for val in df['2020 [YR2020]']]
df['2021 [YR2021]'] = [int(clean_val(val)) for val in df['2021 [YR2021]']]

print(df.head())

df.drop(['2020 [YR2020]', '2021 [YR2021]'], axis=1, inplace=True)

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
df_fit = df[["2018 [YR2018]", "2019 [YR2019]"]].copy()
# normalise dataframe and inspect result. Normalisation is done only on the extracted columns. .copy() prevents
# changes in df_fit to affect df. This make the plots with the original measurements possible
df_fit = norm_df(df_fit)
print(df_fit.describe())

for ic in range(2, 7):
  # set up kmeans and fit
  kmeans = cluster.KMeans(n_clusters=ic)
  kmeans.fit(df_fit)
  # extract labels and calculate silhoutte score
  labels = kmeans.labels_
  print (ic, skmet.silhouette_score(df_fit, labels))

"""Good results for 5 clusters

Plot on normalized values
"""

#Plot for 5 clusters
kmeans = cluster.KMeans(n_clusters=5)
kmeans.fit(df_fit)
# extract labels and cluster centres
labels = kmeans.labels_
cen = kmeans.cluster_centers_
plt.figure(figsize=(6.0, 6.0))
# Individual colours can be assigned to symbols. The label l is used to the select the l-th number from the colour table.
plt.scatter(df_fit["2018 [YR2018]"], df_fit["2019 [YR2019]"], c=labels, cmap="Accent")
# colour map Accent selected to increase contrast between colours
# show cluster centres
for ic in range(2):
  xc, yc = cen[ic,:]
  plt.plot(xc, yc, "dk", markersize=10)

plt.xlabel("2018 [YR2018]")
plt.ylabel("2019 [YR2019]")
plt.title("2 clusters on normalized values")
plt.show()

"""Plot on original values"""

df_sub = df[["2018 [YR2018]", "2019 [YR2019]"]].copy()
df_sub['cluster id'] = kmeans.labels_
df_sub.head()

#Plot for 5 clusters
kmeans = cluster.KMeans(n_clusters=5)
kmeans.fit(df_fit)
# extract labels and cluster centres
labels = kmeans.labels_
cen = kmeans.cluster_centers_
plt.figure(figsize=(6.0, 6.0))
# Individual colours can be assigned to symbols. The label l is used to the select the l-th number from the colour table.
plt.scatter(df_sub["2018 [YR2018]"], df_sub["2019 [YR2019]"], c=df_sub['cluster id'], cmap="Accent")
# colour map Accent selected to increase contrast between colours
# show cluster centres
for ic in range(2):
  xc, yc = cen[ic,:]
  plt.plot(xc, yc, "dk", markersize=10)

plt.xlabel("2018 [YR2018]")
plt.ylabel("2019 [YR2019]")
plt.title("2 clusters on original values")
plt.show()

"""Curve fitting"""

def exp_growth(t, scale, growth):
  """ Computes exponential function with scale and growth as free parameters"""
  f = scale * np.exp(growth * (t-2000))
  return f

df.head(40)

"""Picking afghanistan from cluster 0 and algeria from cluster 2"""

afg = df[df['Country Name'] == 'Afghanistan']
alg = df[df['Country Name'] == 'Algeria']
