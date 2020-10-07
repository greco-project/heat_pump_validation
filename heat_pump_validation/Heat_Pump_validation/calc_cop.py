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
                                                      'results', 'heat_pump'))

# Data from 03.04.2019
try:
    datalogger_1 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190304_temp_diff_all.csv'),
                               parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run HP_pre_processing.py first.\n')

# Resampled data is the mean over an hour of original data
data_resample_1 = datalogger_1.resample('H').mean()

# Data from 01.04.2019
try:
    datalogger_2 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190301_temp_diff_all.csv'),
                               parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run HP_pre_processing.py first.\n')

# Resampled data is the mean over an hour of original data
data_resample_2 = datalogger_2.resample('H').mean()

# Concatenate data of the two dates for original and sampled data
datalogger = pd.concat([datalogger_1, datalogger_2], sort=False)
datalogger_resample = pd.concat([data_resample_1, data_resample_2], sort=False)

# Save
datalogger.to_csv(os.path.join(path_preprocessed_data, 'original', 'data_original.csv'))

temp_high = datalogger['T_air']
temp_high_resampled = datalogger_resample['T_air']
temp_low = datalogger['T_ext']
temp_low_resampled = datalogger_resample['T_ext']

quality_grades = np.arange(0.05, 0.55, 0.05)
cops_heat_pump, cops_heat_pump_resampled = [pd.DataFrame() for variable in range(2)]
cops_heat_pump['Time'] = datalogger.index
cops_heat_pump_resampled['Time'] = datalogger_resample.index


for quality_grade in quality_grades:
    cop_name = str(np.round(quality_grade, 2)).split('.')[1]
    cops_heat_pump['COP_' + cop_name] = cmpr_hp_chiller.calc_cops(temp_high=temp_high,
                                                                  temp_low=temp_low,
                                                                  quality_grade=np.round(quality_grade, 2),
                                                                  mode='heat_pump')

    cops_heat_pump_resampled['COP_' + cop_name] = cmpr_hp_chiller.calc_cops(temp_high=temp_high_resampled,
                                                                            temp_low=temp_low_resampled,
                                                                            quality_grade=np.round(quality_grade, 2),
                                                                            mode='heat_pump')

    print('\nCoefficients of Performance (COP) with quality grade ' + str(np.round(quality_grade, 2)) + ':')
    print(cops_heat_pump_resampled['COP_' + cop_name])


