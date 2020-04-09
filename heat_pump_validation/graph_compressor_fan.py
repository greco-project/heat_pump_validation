import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
tempcontrol = pd.read_csv(
    r'\\fs01\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190304_MPPT_HEATING_TempControl.csv')
datalogger = pd.read_csv(r'\\fs01\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190304_MPPT_HEATING_Datalogger.csv')

datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
datalogger['Time'] = pd.to_datetime(datalogger['Time'])
time = datalogger['Time']
PAC = tempcontrol['P_AC']
list_temp_high = datalogger['T_air '].values.tolist()
list_t_ext = datalogger['T_ext'].values.tolist()

temp_diff_2 = [(t_h - t_ext) for (t_h, t_ext) in zip(list_temp_high, list_t_ext)]
temp_diff_2_series = pd.Series(temp_diff_2, name='temp_diff_2')

concat= pd.concat([time, datalogger['Fan_int '], temp_diff_2_series, PAC], axis=1) #temp_diff_2_series],axis=1)
#concat.to_csv(r'C:\git\data\PV_HeatPump_HEATING\20190304\concat_data.csv')
concat = concat.iloc[3994:4802]

plt.figure()
plt.ylim(-10, 800)
plt.ylabel('T_int_OUT-T_int_IN')
plt.xlabel('Time')
plt.plot(concat['Time'],concat['Fan_int '], color='r')
plt.plot(concat['Time'],concat['temp_diff_2'], color='b')
plt.plot(concat['Time'],concat['P_AC'], color='g')
plt.legend(('integral fan', 'T_int-T_out', 'Compressor'))
plt.savefig(r'\\fs01\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_HeatPump_HEATING\20190304_HEATING_Figure_PAC_v1.png')
plt.close()





