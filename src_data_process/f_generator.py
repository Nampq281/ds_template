from functools import reduce
import pandas as pd
import numpy as np
from src_data_process.utils import create_ym_format, month_diff
from datetime import datetime as dt


def time_travel(df, last_n_months):
    start = (df['last_x_months'] >= 0) 
    end = (df['last_x_months'] <= (last_n_months))
    filter_last_n_mths = (start & end)
    return df[filter_last_n_mths]

def agg_cal(df:pd.DataFrame, 
            groupby:list, 
            aggfunc:dict,
           ):    
    group_df = df.groupby(groupby)
    df = group_df.agg(aggfunc)
    df.columns = [col_name[0]+'_'+col_name[1] for col_name in df.columns]
    return df.reset_index(drop=False)

def generate_feature_lxm(df, 
                         groupby:list, 
                         aggfunc:dict,  
                         LxM:list=[3,6,9]):
    """
        required columns: ['last_x_months']
    """
    result_lst = []
    for mth_counts in LxM: 
        mth_counts += 1 # plus 1 month distance for PCB data to update
        df_lxm = time_travel(df, mth_counts)
        result = agg_cal(df_lxm, groupby, aggfunc)
        feat_col = list(set(result.columns)-set(groupby))
        result.columns = [col+f'_l{mth_counts}m' if col in feat_col else col for col in result.columns]
        result_lst.append(result)
        
    final_df = reduce(lambda  left,right: pd.merge(left, right, on=groupby, how='outer'), result_lst)
    return final_df



# def rule_pcb_info(df, fil_col:list):
#     """
#     Only use report that last updated last 6 months until now
#     input column: DateOfLastUpdate (PCB), CreditLimit, ResidualAmount
#     """
#     df['UpdateDateFmt'] = create_ym_format(df, 'CommonData.DateOfLastUpdate', fmt='%d%m%Y')
#     df['mth_snc_last_update'] = df.apply(lambda row: month_diff(row['UpdateDateFmt'], dt.today()), axis=1)

#     df_filtered = df.copy()
#     most_update_filter = (df_filtered['mth_snc_last_update'].isna())|(df_filtered['mth_snc_last_update']>6)
#     # if contract is last updated in the past >6 months -> not include in calculation
#     df_filtered.loc[most_update_filter, fil_col] = np.nan
#     return df_filtered