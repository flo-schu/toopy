import pandas as pd
import itertools as it

def read_csv_list(filenames, kwargs={}):
    df = pd.DataFrame()
    for filename in filenames:
        df = df.append(pd.read_csv(filename, **kwargs))
    return df

def expand_grid(data_dict):
    """Create a dataframe from every combination of given values."""
    rows = it.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def flatten_columns_and_replace(df, search=None, replace=None):
    collist = [a+b for a, b in list(df.columns.to_flat_index())]
    collist = [colname.replace(search, replace) for colname in collist]
    df.columns = collist
    return df