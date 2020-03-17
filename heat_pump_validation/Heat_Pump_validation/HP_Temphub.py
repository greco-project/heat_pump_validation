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


datalogger = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\calc_COP_original.csv')
datalogger_resampled = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\calc_COP_all_resampled.csv')

validation_data = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\data_original.csv')
validation_data_resampled = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\data_resampled.csv')

validation_data['Time'] = validation_data['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
validation_data['Time'] = pd.to_datetime(validation_data['Time'])

validation_data_resampled['Time'] = validation_data_resampled['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
validation_data_resampled['Time'] = pd.to_datetime(validation_data_resampled['Time'])

# temphub = temphub(t_high_series=validation_data['T_int'],
#                   t_low_series=validation_data['T_ext '])

temphub_resampled= temphub(t_high_series=validation_data_resampled['T_int'],
                           t_low_series=validation_data_resampled['T_ext '])

validation_series = validation_data['COP']

validation_series_resampled = validation_data_resampled['COP']

# final_data = pd.concat([datalogger, temphub, validation_series], axis=1,
#                  names=['Time', 'COP']).set_index('Time')

final_data_resampled = pd.concat([datalogger_resampled,
                                  temphub_resampled, validation_series_resampled], axis=1,
                                 names=['Time', 'COP']).set_index('Time')

final_data_resampled.to_csv(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\final_data_resampled.csv')
#final_data.to_csv(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\final_data.csv')
