import pandas as pd

r"""
temp_diff: T_air/T_int_OUT - T_int_IN
internal fan turns off, leading to a negative or small difference

temp_diff_2: T_air/T_int_OUT - T_ext_IN
[...], leading to small or negative differences 

 """

datalogger = pd.read_csv(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190304_MPPT_HEATING_Datalogger.csv',
                         encoding='unicode_escape', low_memory=False)
tempcontrol = pd.read_csv(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190304_MPPT_HEATING_TempControl.csv',
                          encoding='unicode_escape', low_memory=False)

datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
datalogger['Time'] = pd.to_datetime(datalogger['Time'])
list_temp_high = datalogger['T_air '].values.tolist()
list_temp_low = datalogger['T_int '].values.tolist()
list_t_ext = datalogger['T_ext'].values.tolist()

temp_diff = [(t_h - t_l) for (t_h, t_l) in zip(list_temp_high, list_temp_low)]
temp_diff_series = pd.Series(temp_diff, name='temp_diff')

temp_diff_2 = [(t_h - t_ext) for (t_h, t_ext) in zip(list_temp_high, list_t_ext)]
temp_diff_2_series = pd.Series(temp_diff_2, name='temp_diff_2')



tempcontrol.loc[tempcontrol.COP == 0, 'COP'] = None
dataframe = pd.concat([datalogger['Time'], tempcontrol['COP'], datalogger['T_air '],
                       datalogger['T_ext'], datalogger['T_int '], temp_diff_series,
                       temp_diff_2_series], axis=1).set_index('Time')
dataframe.loc[dataframe.temp_diff < 5, 'temp_diff'] = None
dataframe.loc[dataframe.temp_diff_2 < 5, 'temp_diff_2'] = None
temp_diff_data = dataframe.dropna()
temp_diff_data.to_csv(r'C:\git\data\PV_HeatPump_HEATING\20190304\20190304_temp_diff_all.csv')
print(temp_diff_data)

