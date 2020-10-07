import pandas as pd
import numpy as np

datalogger = pd.read_csv(r'\\fs01\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190712_TempControl_COOLING_SP18_Datalogger.csv')
tempcontrol = pd.read_csv(r'\\fs01\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Data\UPM\csv\20190712_TempControl_COOLING_SP18_TempControl.csv')
Text = datalogger['T_ext_IN']
Tint = datalogger['Tint_IN ']
Tint_out = datalogger['T_int_OUT']
measured_eer = tempcontrol['EER']

datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
datalogger['Time'] = pd.to_datetime(datalogger['Time'])

data = pd.concat([datalogger['Time'], Text, Tint, Tint_out, measured_eer], axis=1,
                 names=['Time', 'T_ext_IN', 'T_in_IN', 'T_int_OUT', 'EER']).set_index('Time')
data_nan = data.replace(0, np.nan).dropna()
data_resampled = data_nan.resample('H').mean()
data_resampled.to_csv(r'C:\git\data\PV_Chiller_COOLING\20190712_COOLING_temp_re.csv')

