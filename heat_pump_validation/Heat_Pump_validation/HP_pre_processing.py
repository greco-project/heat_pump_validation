import pandas as pd
import numpy as np
import os

r"""
T_air = T_int_OUT
temp_diff: T_air - T_int_IN
integral fan turns off, leading to a negative or small difference

temp_diff_2: T_air - T_ext_IN
compressor shuts down, leading to small or negative differences 

 """

# Choose the date written in the file name you want to examine
dates = np.array(['20190301', '20190304'])


def fix_param_name(data, name):
    """
    This function fixes bugs in the naming of the parameters
    :param name:
    """
    try:
        data.rename(columns={name + ' ': name}, inplace=True)
    except KeyError:
        print('Value ' + name + ' not in table. Please check.')


def preprocess_heat_pump_data(date_string):
    # Set paths
    path_file = os.path.dirname(__file__)
    path_raw_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir, 'raw_data'))
    path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                          'results', 'heat_pump', 'original'))

    # Read original data of datalogger
    datalogger = pd.read_csv(os.path.join(path_raw_data, date_string + '_MPPT_HEATING_Datalogger.csv'),
                             low_memory=False)
    # Read original data of tempcontrol
    tempcontrol = pd.read_csv(os.path.join(path_raw_data, date_string + '_MPPT_HEATING_TempControl.csv'),
                              low_memory=False)

    # Adjust parameter naming for the parameters needed in this file
    fix_param_name(datalogger, 'T_ext')
    fix_param_name(datalogger, 'T_int')
    fix_param_name(datalogger, 'T_air')

    # Change format of 'Time' to datetime format
    datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
    datalogger['Time'] = pd.to_datetime(datalogger['Time'])

    # Write values of temperatures to list
    list_temp_high = datalogger['T_air'].values.tolist()  # External temperature of compressor
    list_temp_low = datalogger['T_ext'].values.tolist()  # External temperature of evaporator
    list_temp_medium = datalogger['T_int'].values.tolist()  # External temperature of condenser

    # Calculate temperature difference between compressor and condenser
    temp_diff = [(t_h - t_m) for (t_h, t_m) in zip(list_temp_high, list_temp_medium)]
    temp_diff_series = pd.Series(temp_diff, name='temp_diff')

    # Calculate temperature difference between compressor and evaporator
    temp_diff_2 = [(t_h - t_l) for (t_h, t_l) in zip(list_temp_high, list_temp_low)]
    temp_diff_2_series = pd.Series(temp_diff_2, name='temp_diff_2')

    # Calculate temperature difference between condenser and evaporator
    temp_diff_3 = [(t_m - t_l) for (t_m, t_l) in zip(list_temp_medium, list_temp_low)]
    temp_diff_3_series = pd.Series(temp_diff_3, name='temp_diff_3')

    # Convert values where COP = 0 to None
    tempcontrol.loc[tempcontrol.COP == 0, 'COP'] = None

    # Concatenate measured values with 'Time' column
    dataframe = pd.concat([datalogger['Time'], tempcontrol['COP'], datalogger['T_comp(ºC)'],
                           datalogger['T_evap (ºC)'], datalogger['T_cond (ºC)'], datalogger['Tint-Text (ºC)'],
                           datalogger['T_air'], datalogger['T_ext'], datalogger['T_int'], temp_diff_series,
                           temp_diff_2_series, temp_diff_3_series], axis=1).set_index('Time')

    # Convert temperature differences that are smaller than 5 °C to None values
    dataframe.loc[dataframe.temp_diff < 5, 'temp_diff'] = None
    dataframe.loc[dataframe.temp_diff_2 < 5, 'temp_diff_2'] = None
    dataframe.loc[dataframe.temp_diff_3 < 5, 'temp_diff_3'] = None

    # Drop every None value from cleaned data
    cleaned_data = dataframe.dropna()

    # Print how much data has been cleaned
    #print('\nDate: ', date_string,
    #      '\nData points raw data: ', len(datalogger),
    #      '\nData points preprocessed: ', len(cleaned_data),
    #      '\nRelation of cleaned data to whole data: ', (len(datalogger) - len(cleaned_data)) / len(datalogger), '\n')

    # Export data to csv
    cleaned_data.to_csv(os.path.join(path_preprocessed_data, date_string + '_temp_diff_all.csv'))

    # Print data
    print('Preprocessed data: ', os.path.join(path_preprocessed_data, date_string + '_temp_diff_all.csv'))


for item in dates:
    preprocess_heat_pump_data(item)
