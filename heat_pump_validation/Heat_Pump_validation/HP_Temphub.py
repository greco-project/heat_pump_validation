import pandas as pd
import numpy as np

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

validation_data['Time'] = validation_data['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
validation_data['Time'] = pd.to_datetime(validation_data['Time'])

validation_data_resampled['Time'] = validation_data_resampled['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
validation_data_resampled['Time'] = pd.to_datetime(validation_data_resampled['Time'])


temphub_resampled= temphub(t_high_series=validation_data_resampled['T_int'],
                           t_low_series=validation_data_resampled['T_ext '])

validation_series_resampled = validation_data_resampled['COP']


final_data_resampled = pd.concat([datalogger_resampled,
                                  temphub_resampled, validation_series_resampled], axis=1,
                                 names=['Time', 'COP']).set_index('Time')

# Print data
