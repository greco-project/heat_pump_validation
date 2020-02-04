import pandas as pd
import numpy as np

''''
Temphub calculation
* Input: calculated EER/COP, Time from original data
* validation_data: measured EER
'''


def temphub(t_high_series, t_low_series):
    t_high_list = t_high_series.values.tolist()
    t_low_list = t_low_series.values.tolist()

    temphub = [(t_h - t_l) for (t_h, t_l) in zip(t_high_list, t_low_list)]
    temphub_series = pd.Series(temphub, name='Temphub')

    return temphub_series


EER_data = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\calc_cop_Tint_OUT\20190301_calc_cop.csv')  # alle berechneten EER 03-05
time_data = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\20190301_TempControl_HEATING_SP18_Datalogger.csv')
validation_data = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\20190301_TempControl_HEATING_SP18_MPPT.csv',
                              encoding='unicode_escape', low_memory=False)

time_data['Time'] = time_data['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
time_data['Time'] = pd.to_datetime(time_data['Time'])

temphub = temphub(time_data['T_ext'], time_data['T_air '])  # calc temphub
validation_series = validation_data['COP']

# resample every 30 minutes / 1 hour and concatenated with temphub and COP/EER
data = pd.concat([time_data['Time'], EER_data, temphub, validation_series], axis=1,
                 names=['Time', 'COP']).set_index('Time')
data_nan = data.replace(0, np.nan).dropna()
data_resampled = data_nan.resample('H').mean()
data_resampled.to_csv(r'C:\git\data\PV_HeatPump_HEATING\calc_cop_Tint_OUT\20190301_Tint_OUT_Temphub_T_air\resampled.csv')
data_nan.to_csv(r'C:\git\data\PV_HeatPump_HEATING\calc_cop_Tint_OUT\20190301_Tint_OUT_Temphub_T_air\20190301_all_data.csv')
