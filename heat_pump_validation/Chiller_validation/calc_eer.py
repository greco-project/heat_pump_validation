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
try:
    datalogger_1 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190711_COOLING_temp.csv'),
                               parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_SP18.py first.\n')
try:
    datalogger_resampled_1 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled',
                                                      '20190711_COOLING_temp_re.csv'), parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_SP18.py first.\n')

try:
    datalogger_2 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190712_COOLING_temp.csv'),
                           parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_SP18.py first.\n')

try:
    datalogger_resampled_2 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled',
                                                      '20190712_COOLING_temp_re.csv'), parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_SP18.py first.\n')

try:
    datalogger_3 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190115_COOLING_temp.csv'),
                               parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_MPPT.py first.\n')

try:
    datalogger_resampled_3 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled',
                                                      '20190115_COOLING_temp_re.csv'), parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_MPPT.py first.\n')

try:
    datalogger_4 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190120_COOLING_temp.csv'),
                               parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_MPPT.py first.\n')

try:
    datalogger_resampled_4 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled',
                                                      '20190120_COOLING_temp_re.csv'), parse_dates=True, index_col=0)
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_MPPT.py first.\n')

# Concatenate data of the two dates for original and sampled data
datalogger = pd.concat([datalogger_1, datalogger_2, datalogger_3, datalogger_4])
datalogger_resampled = pd.concat([datalogger_resampled_1, datalogger_resampled_2,
                                  datalogger_resampled_3, datalogger_resampled_4])

# Save
datalogger.to_csv(os.path.join(path_preprocessed_data, 'original', 'data_original.csv'))
datalogger_resampled.to_csv(os.path.join(path_preprocessed_data, 'resampled', 'data_resampled.csv'))

temp_high = datalogger['T_ext']
temp_high_resampled = datalogger_resampled['T_ext']
temp_low = datalogger['T_air']
temp_low_resampled = datalogger_resampled['T_air']

dataseries = pd.DataFrame(cops_chiller)


    print('\nEnergy Efficiency Ratio (EER) with quality grade ' + str(np.round(quality_grade, 2)) + ':')

# print("")
# print("Coefficients of Performance (COP): ", *cops_chiller, sep='\n')
# print("")

