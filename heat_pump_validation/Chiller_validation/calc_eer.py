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

quality_grades = np.arange(0.05, 0.55, 0.05)
eer_chiller, eer_chiller_resampled = [pd.DataFrame() for variable in range(2)]
eer_chiller['Time'] = datalogger.index
eer_chiller_resampled['Time'] = datalogger_resampled.index

for quality_grade in quality_grades:
    eer_name = str(np.round(quality_grade, 2)).split('.')[1]
    eer_chiller['EER_' + eer_name] = cmpr_hp_chiller.calc_cops(temp_high=temp_high,
                                                               temp_low=temp_low,
                                                               quality_grade=np.round(quality_grade, 2),
                                                               mode='chiller')

    eer_chiller_resampled['EER_' + eer_name] = cmpr_hp_chiller.calc_cops(temp_high=temp_high_resampled,
                                                                         temp_low=temp_low_resampled,
                                                                         quality_grade=np.round(quality_grade, 2),
                                                                         mode='chiller')

    print('\nEnergy Efficiency Ratio (EER) with quality grade ' + str(np.round(quality_grade, 2)) + ':')
    print(eer_chiller_resampled['EER_' + eer_name])

eer_chiller.to_csv(os.path.join(path_preprocessed_data, 'original', 'calc_eer_all_Tint_OUT.csv'),
                   decimal='.', index=False)
eer_chiller_resampled.to_csv(os.path.join(path_preprocessed_data, 'resampled', 'calc_eer_all_Tint_OUT_re.csv'),
                             decimal='.', index=False)

