"""
Example on how to use the 'calc_cops' function to get the
COPs of a compression chiller.

We use the ambient air as heat sink (high temperature reservoir). The input is
a list to show how the function can be applied on several time steps. The
output is a list as well and may serve as input (conversion_factor) for a
oemof.solph.transformer.
"""

import src.oemof.thermal.compression_heatpumps_and_chillers as cmpr_hp_chiller
import pandas as pd

datalogger = pd.read_csv(r'C:\git\data\20190711_TempControl_COOLING_SP18_Datalogger.csv')
data_t_high = datalogger['T_ext_IN']
data_t_low = datalogger['T_int_OUT']

data_t_high_list = data_t_high.values.tolist()
data_t_low_list = data_t_low.values.tolist()



cops_chiller = cmpr_hp_chiller.calc_cops(t_high= data_t_high_list,
                                         t_low= data_t_low_list,
                                         quality_grade=0.3,
                                         mode='chiller')
dataseries = pd.DataFrame(cops_chiller)

dataseries.to_csv(r'C:\git\data\20190711\EER_03.csv', decimal='.')

print("")
print("Coefficients of Performance (COP): ", *cops_chiller, sep='\n')
print("")


