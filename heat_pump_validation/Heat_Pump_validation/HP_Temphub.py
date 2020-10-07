import pandas as pd
import os


def temphub(t_high_series, t_low_series):
    r"""
    Calculates the temphub with t_high as heat source and t_low as heat sink
    Parameters
    ----------

    :param t_high_series: pd.Series
    :param t_low_series: pd.Series

    :returns
    --------

    pd.Series
    """
    t_high_list = t_high_series.values.tolist()
    t_low_list = t_low_series.values.tolist()

    temphub = [(t_l - t_h) for (t_l, t_h) in zip(t_low_list, t_high_list)]
    temphub_series = pd.Series(temphub, name='Temphub')

    return temphub_series


# Set paths
path_file = os.path.dirname(__file__)
path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                      'results', 'heat_pump'))

# Get COP calculations
try:
    datalogger = pd.read_csv(os.path.join(path_preprocessed_data, 'original', 'calc_COP_original.csv'))
    datalogger_resampled = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', 'calc_COP_all_resampled.csv'))
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run calc_cop.py first.\n')

# Get original and resampled data
try:
    validation_data = pd.read_csv(os.path.join(path_preprocessed_data, 'original', 'data_original.csv'))
    validation_data_resampled = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', 'data_resampled.csv'))
except FileNotFoundError:
    print('\nData could not be read. It may not exist yet. Please run calc_cop.py first.\n')

# Convert 'Time' to datetime
validation_data['Time'] = validation_data['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
validation_data['Time'] = pd.to_datetime(validation_data['Time'])
validation_data_resampled['Time'] = validation_data_resampled['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
validation_data_resampled['Time'] = pd.to_datetime(validation_data_resampled['Time'])

# Calculate Temperaturhub
temphub_value = temphub(t_high_series=validation_data['T_air'],
                        t_low_series=validation_data['T_ext'])
temphub_value_resampled = temphub(t_high_series=validation_data_resampled['T_air'],
                                  t_low_series=validation_data_resampled['T_ext'])


# Get 'COP' of original and sampled data
validation_series = validation_data['COP']
validation_series_resampled = validation_data_resampled['COP']


final_data = pd.concat([datalogger, temphub_value, validation_series],
                       axis=1, names=['Time', 'COP']).set_index('Time')
final_data_resampled = pd.concat([datalogger_resampled, temphub_value_resampled, validation_series_resampled],
                                 axis=1, names=['Time', 'COP']).set_index('Time')

final_data.to_csv(os.path.join(path_preprocessed_data, 'original', 'final_data.csv'))
final_data_resampled.to_csv(os.path.join(path_preprocessed_data, 'resampled', 'final_data_resampled.csv'))

# Print data
print('\nFinal original data: ', os.path.join(path_preprocessed_data, 'original', 'final_data.csv'))
print('\nFinal resampled data: ', os.path.join(path_preprocessed_data, 'resampled', 'final_data_resampled.csv'))
