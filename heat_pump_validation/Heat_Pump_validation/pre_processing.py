import pandas as pd

r"""
T_air - T_ext needs to be larger than 5
 """

datalogger = pd.read_csv(r'',
                         encoding='unicode_escape', low_memory=False)
tempcontrol = pd.read_csv(r'',
                          encoding='unicode_escape', low_memory=False)

datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
datalogger['Time'] = pd.to_datetime(datalogger['Time'])
list_temp_high = datalogger['T_air '].values.tolist()
list_temp_low = datalogger['T_ext'].values.tolist()

temp_diff = [(t_h - t_l) for (t_h, t_l) in zip(list_temp_high, list_temp_low)]
temp_diff_series = pd.Series(temp_diff, name='temp_diff')

tempcontrol.loc[tempcontrol.COP == 0, 'COP'] = None
dataframe = pd.concat([datalogger['Time'], tempcontrol['COP'], temp_diff_series], axis=1).set_index('Time')
dataframe.loc[dataframe.temp_diff < 5, 'temp_diff'] = None
temp_diff_data = dataframe.dropna()

temp_diff_data.to_csv(r'C:\git\data\PV_HeatPump_HEATING\20190304\20190304_temp_diff_data.csv')
print(temp_diff_data)

