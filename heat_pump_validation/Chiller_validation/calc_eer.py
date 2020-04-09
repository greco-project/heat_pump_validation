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


datalogger_resampled= pd.read_csv(r'file:///C:\git\data\PV_Chiller_COOLING\COOLING_temp_re.csv')


temp_high = datalogger_resampled['T_ext_IN ']
temp_low = datalogger_resampled['T_int_OUT ']


cops_chiller = cmpr_hp_chiller.calc_cops(temp_high= temp_high,
                                         temp_low= temp_low,
                                         quality_grade=0.4,
                                         mode='heat_pump')

dataseries = pd.DataFrame(cops_chiller)


dataseries.to_csv(r'C:\git\data\PV_Chiller_COOLING\COP\EER_4.csv', decimal='.')

# print("")
# print("Coefficients of Performance (COP): ", *cops_chiller, sep='\n')
# print("")

