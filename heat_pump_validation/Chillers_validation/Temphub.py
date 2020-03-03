import pandas as pd
import numpy as np


def temphub(t_high_series, t_low_series):
    r"""
    Calculates the temphub with t_high as heat source and t_low as Wärmesenke(?)
    Parameters
    ----------

    :param t_high_series: pd.Series
    :param t_low_series: pd.Series

    :returns
    --------

    pd.Series
    """
    t_high_list = t_high_series.values.tolist()
    t_low_list = t_low_series.values.tolist()

    temphub = [(t_l - t_h) for (t_l, t_h) in zip(t_low_list, t_high_list)]
    temphub_series = pd.Series(temphub, name='Temphub')

    return temphub_series

r"""
read data and reformat time to datetime

Parameters
----------
EER_data: pd.DataFrame
calculated EER

time_data: pd.DataFrame
read time from Datalogger data

validation_data: pd.DataFrame
read measured EER from Tempcontrol data

:returns
--------

data_nan: pd.DataFrame
drop all rows filled with NaNs 

data_resampled: pd.Dataframe
resample of data_nan for every hour  

"""
EER_data = pd.read_csv(r'file:///C:\git\data\PV_Chiller_COOLING\20190712\calc_EER_Tint_IN\20190712_calc_EER.csv')
time_data = pd.read_csv(r'file:///C:\git\data\20190712_TempControl_COOLING_SP18_Datalogger.csv')
validation_data = pd.read_csv(r'file:///C:\git\data\20190712_TempControl_COOLING_SP18_TempControl.csv',
                              encoding='unicode_escape', low_memory=False)

time_data['Time'] = time_data['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
time_data['Time'] = pd.to_datetime(time_data['Time'])

temphub = temphub(t_high_series=time_data['T_ext_IN'], t_low_series=time_data['T_int_IN'])
validation_series = validation_data['EER']

data = pd.concat([time_data['Time'], EER_data, temphub, validation_series], axis=1,
                 names=['Time', 'EER']).set_index('Time')
data_nan = data.replace(0, np.nan).dropna()
data_resampled = data_nan.resample('H').mean()
data_resampled.to_csv(r'')
data_nan.to_csv(r'')


