import pandas as pd
import numpy as np
from tqdm import tqdm

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

from math import ceil
from functools import wraps, reduce

import logging

def log_step(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tic = dt.now()
        result = func(*args, **kwargs)
        time_taken = str(dt.now() - tic)
        print(f"[{func.__name__}] Shape:{result.shape}. Process time: {time_taken}s")
        return result
    return wrapper
    
def ym_format(input_str, fmt):
    try: 
        output_dt = dt.strptime(str(input_str), fmt)
    except:
        output_dt = np.nan
    return output_dt

def create_ym_format(df, ym_col, fmt='%Y%m'):
    return df[ym_col].apply(lambda row: ym_format(row, fmt))
 
def month_diff(start, end):
  try:
      return ceil((end - start).days / 30.436875)
  except:
      return np.nan      

def format_start_date(row):
    if len(str(row))<7:
        row = None
    else:
         row = '0'+str(row) if len(str(row))<8 else str(row)
    return row

def get_dt_format(row):
    try:
        dt_type = dt.strptime(row, '%d%m%Y')
    except:
        dt_type = None
    return dt_type
    



