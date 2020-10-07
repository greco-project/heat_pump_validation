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

# Set paths
path_file = os.path.dirname(__file__)
path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                      'results', 'chiller'))

# Read data original and resampled from 11.07.2019 and 12.07.2019


temp_high = datalogger_resampled['T_ext_IN ']
temp_low = datalogger_resampled['T_int_OUT ']


cops_chiller = cmpr_hp_chiller.calc_cops(temp_high= temp_high,
                                         temp_low= temp_low,
                                         quality_grade=0.4,
                                         mode='heat_pump')

dataseries = pd.DataFrame(cops_chiller)


    print('\nEnergy Efficiency Ratio (EER) with quality grade ' + str(np.round(quality_grade, 2)) + ':')

# print("")
# print("Coefficients of Performance (COP): ", *cops_chiller, sep='\n')
# print("")

