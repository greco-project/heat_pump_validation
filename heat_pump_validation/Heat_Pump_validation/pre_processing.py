import pandas as pd

r"""
Sort out unfitting data
 """

datalogger = pd.read_csv(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190301_MPPT_HEATING_Datalogger.csv',
                         encoding='unicode_escape', low_memory=False)
tempcontrol = pd.read_csv(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190301_MPPT_HEATING_TempControl.csv',
                          encoding='unicode_escape', low_memory=False)

datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
datalogger['Time'] = pd.to_datetime(datalogger['Time'])
list_temp_high = datalogger['T_air'].values.tolist()
list_temp_low = datalogger['T_ext '].values.tolist()

temp_diff = [(t_h - t_l) for (t_h, t_l) in zip(list_temp_high, list_temp_low)]
temp_diff_series = pd.Series(temp_diff, name='temp_diff')

tempcontrol.loc[tempcontrol.COP == 0, 'COP'] = None
dataframe = pd.concat([datalogger['Time'], tempcontrol['COP'], datalogger['T_air'],
                       datalogger['T_ext '], datalogger['T_int'], temp_diff_series], axis=1).set_index('Time')
dataframe.loc[dataframe.temp_diff < 5, 'temp_diff'] = None
temp_diff_data = dataframe.dropna()
temp_diff_data.to_csv(r'C:\git\data\PV_HeatPump_HEATING\20190301\20190301_temp_diff_data.csv')
print(temp_diff_data)

