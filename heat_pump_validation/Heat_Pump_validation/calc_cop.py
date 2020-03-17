"""
Example on how to use the 'calc_cops' function to get the
COPs of a compression chiller.

We use the ambient air as heat sink (high temperature reservoir). The input is
a list to show how the function can be applied on several time steps. The
output is a list as well and may serve as input (conversion_factor) for a
oemof.solph.transformer.
"""

import oemof.thermal.compression_heatpumps_and_chillers as cmpr_hp_chiller
import pandas as pd


datalogger_1= pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\20190304\20190304_temp_diff_all.csv',
                          parse_dates=True, index_col=0)
data_resample_1 = datalogger_1.resample('H').mean()
datalogger_2 = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\20190301\20190301_temp_diff_all.csv',
                           parse_dates=True, index_col=0)
data_resample_2 = datalogger_2.resample('H').mean()

datalogger = pd.concat([datalogger_1, datalogger_2])
datalogger_resample = pd.concat([data_resample_1, data_resample_2])
# datalogger.to_csv(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\data_original.csv')
# datalogger_resample.to_csv(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\data_resampled.csv')

temp_high = datalogger_resample['T_air']
temp_low = datalogger_resample['T_ext ']

#data_t_high_list = data_t_high.values.tolist()
#data_t_low_list = data_t_low.values.tolist()

cops_chiller = cmpr_hp_chiller.calc_cops(temp_high= temp_high,
                                         temp_low= temp_low,
                                         quality_grade=0.4,
                                         mode='heat_pump')

dataseries = pd.DataFrame(cops_chiller)


dataseries.to_csv(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\COP_resampled\COP_4.csv', decimal='.')

# print("")
# print("Coefficients of Performance (COP): ", *cops_chiller, sep='\n')
# print("")

