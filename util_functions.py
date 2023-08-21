import pandas as pd
import numpy as np
import os
from pathlib import Path

def drop_columns(df, features_to_drop):
  df_columns = list(df.columns)
  df_columns = list(map(lambda x: x.lower(), df_columns))
  columns_to_drop_from_df = [features_to_drop[i] for i in range(len(features_to_drop)) if features_to_drop[i].lower() in df_columns]
  return df.drop(columns_to_drop_from_df, axis=1)

def load_and_clean_dataset(filename):
  filename_path = Path(filename)
  if filename_path.suffix == '.csv':
    df = pd.read_csv(filename, index_col=None)
  elif filename_path.suffix == '.xlsx':
    df = pd.read_excel(filename, index_col=None)
  df_null = df[df['CONTROL_PROBE_TEMP'].isnull()]
  if (len(df_null) > 0):
    df = df.loc[0:df_null.index[0]-1]
  columns_to_drop = ['Date','Time', 'Minutes']
  return drop_columns(df, columns_to_drop)

def aggregated_ind_dataframes(df):
  group_by_control_probe = df.groupby(df['CONTROL_PROBE_TEMP'].astype(float).astype(int))
  return group_by_control_probe.agg([np.min, np.mean, np.max])

def combined_df(frames):
  return pd.concat(frames)

def output_final_df(df_for_single_temperature_list):
  return pd.concat(df_for_single_temperature_list, ignore_index=True)
  
def output_file(filename, df):
  output_file_path = Path.cwd() / 'output_datasets'
  os.chdir(output_file_path)
  df.to_excel(filename)
  os.chdir(output_file_path.parent)
  

# @params -> stacked_df
# pass in a stacked version of the dataframe for each temperature aggregated by [min, mean, max]
# stacked_df - changes columns from multi-index to single index
# with the unstacked version - had trouble accessing multi-index columns
# 
# @method ->
# Every subsequent row has min, mean, max
# Append values in respective np.arrays
def aggregate_min_mean_max(stacked_df):
  len_stacked_df = len(stacked_df)
  min = []
  mean = []
  max = []
  i = 0
  while (i + 2 < len_stacked_df):
    min.append(list(stacked_df.iloc[i]))
    mean.append(list(stacked_df.iloc[i + 1]))
    max.append(list(stacked_df.iloc[i + 2]))
    i += 3
  return (min, mean, max)

# @params -> np_arr, op
# np_arr -> consolidated array 
# op -> str indiciating min, mean, max
#
# @method ->
# Take the min, mean, max of each np.array along axis=0 to give results for every column
def consolidate_min_mean_max_to_1D(np_arr, op):
  if op == 'min':
    return np.min(np_arr, axis=0)
  elif op == 'mean':
    return np.mean(np_arr, axis=0)
  elif op == 'max':
    return np.max(np_arr, axis=0)
  

# @params -> stacked_df, columns, temperature
# columns -> Columns of the original dataframe e.g 1ST_COMP_DISC_PRESS, 1ST_COMP_SUCT_PRESS ...
# TO DO: Does the order of the columns matter? - The order of columns is important
# temperature -> the CONTROL PROBE TEMPERATURE the stacked_df was grouped by
# 
# @method ->
# Output a single dataframe for each temperature
# This is done by - 
# Initialize dictionary with multi-index
#   index_1 : name of column
#   index_2 : labels of min, mean, max
def output_dataframe_for_single_temperature(stacked_df, columns, temperature):
  min_mean_max = aggregate_min_mean_max(stacked_df)
  min_ = consolidate_min_mean_max_to_1D(min_mean_max[0], 'min')
  mean_ = consolidate_min_mean_max_to_1D(min_mean_max[1], 'mean')
  max_ = consolidate_min_mean_max_to_1D(min_mean_max[2], 'max')

  min_mean_max_labels = ['min', 'mean', 'max']
  data_arr = []
  for i,j,k in zip(min_, mean_, max_):
    data= {'min': i, 'mean': j, 'max': k} # data for one column e.g 1ST_COMP_DISC_PRESS 
    data_arr.append(data)

  d = {}
  for i in range(len(columns)):
    column = columns[i]
    for j in range(len(min_mean_max_labels)):
      d[(column, min_mean_max_labels[j])] = [data_arr[i][min_mean_max_labels[j]]]
  df = pd.DataFrame(d)
  df.insert(0, "Temperature", temperature)
  df.set_index(df["Temperature"])
  return df

