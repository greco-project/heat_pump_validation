import pandas as pd
import numpy as np

''''
In this .py EER/COP were calculated first. After that the time was resampled.
EER_03: Calculated EER with quality grade 0,3, T_ext_in and T_int_OUT
'''


# calc temphub
def temphub(t_high_series, t_low_series):
    t_high_list = t_high_series.values.tolist()
    t_low_list = t_low_series.values.tolist()

    temphub = [(t_l - t_h) for (t_l, t_h) in zip(t_low_list, t_high_list)]
    temphub_series = pd.Series(temphub, name='Temphub')

    return temphub_series


EER_data = pd.read_csv(r'file:///C:\git\data\PV_Chiller_COOLING\20190712\calc_EER_Tint_IN\20190712_calc_EER.csv')  # alle berechneten EER 03-05
time_data = pd.read_csv(r'file:///C:\git\data\20190712_TempControl_COOLING_SP18_Datalogger.csv')
validation_data = pd.read_csv(r'file:///C:\git\data\20190712_TempControl_COOLING_SP18_TempControl.csv',
                              encoding='unicode_escape', low_memory=False)

time_data['Time'] = time_data['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
time_data['Time'] = pd.to_datetime(time_data['Time'])

temphub = temphub(t_high_series=time_data['T_ext_IN'], t_low_series=time_data['T_int_IN'])  # calc temphub
validation_series = validation_data['EER']

# resample every 30 minutes / 1 hour and concatenated with temphub and
data = pd.concat([time_data['Time'], EER_data, temphub, validation_series], axis=1,
                 names=['Time', 'EER']).set_index('Time')
data_nan = data.replace(0, np.nan).dropna()
data_resampled = data_nan.resample('H').mean()
data_resampled.to_csv(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\Revised\20190712resampled.csv')
data_nan.to_csv(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\Revised\20190712all_data.csv')
