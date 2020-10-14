import pandas as pd
import numpy as np
import os
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Choose the date written in the file name you want to examine
dates = np.array(['20190115', '20190120'])


def fix_param_name(data, name):
    """
    This function fixes bugs in the naming of the parameters
    :param name:
    """
    try:
        data.rename(columns={name + ' ': name}, inplace=True)
    except KeyError:
        raise KeyError('Value ' + name + ' not in table. Please check.')


def preprocess_chiller_data(date_string):
    # Set paths
    path_file = os.path.dirname(__file__)
    path_raw_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir, 'raw_data'))
    path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                          'results', 'chiller'))

    datalogger = pd.read_csv(os.path.join(path_raw_data, date_string + '_MPPT_COOLING_Datalogger.csv'))
    tempcontrol = pd.read_csv(os.path.join(path_raw_data, date_string + '_MPPT_COOLING_Tempcontrol.csv'))

    datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
    datalogger['Time'] = pd.to_datetime(datalogger['Time'])

    # Adjust parameter naming for the parameters needed in this file
    fix_param_name(datalogger, 'T_ext')
    fix_param_name(datalogger, 'T_int')
    fix_param_name(datalogger, 'T_air')


    # Write values of temperatures to list
    list_temp_high = datalogger['T_ext'].values.tolist()    # External temperature of compressor
    list_temp_low = datalogger['T_air'].values.tolist()     # External temperature of evaporator
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

    # Convert values where EER = 0 to None
    tempcontrol.loc[tempcontrol.EER == 0, 'EER'] = None

    data = pd.concat([datalogger['Time'], datalogger['T_ext'], datalogger['T_int'],
                      datalogger['T_air'], tempcontrol['EER'], temp_diff_series,
                      temp_diff_2_series, temp_diff_3_series], axis=1,
                     names=['Time', 'T_ext', 'T_int', 'T_air', 'EER']).set_index('Time')
    data_nan = data.replace(0, np.nan).dropna()

    # Convert temperature differences that are smaller than 5 °C to None values
    data_nan.loc[data_nan.temp_diff < 5, 'temp_diff'] = None
    data_nan.loc[data_nan.temp_diff_2 < 5, 'temp_diff_2'] = None
    data_nan.loc[data_nan.temp_diff_3 < 5, 'temp_diff_3'] = None

    # Drop every None value from cleaned data
    cleaned_data = data_nan.dropna().iloc[:, 0:4]

    # Print how much data has been cleaned
    #print('\nDate: ', date_string,
    #      '\nData points raw data: ', len(datalogger),
    #      '\nData points preprocessed: ', len(cleaned_data),
    #      '\nRelation of cleaned data to whole data: ', (len(datalogger) - len(cleaned_data)) / len(datalogger), '\n')

    # Export original data to csv
    cleaned_data.to_csv(os.path.join(path_preprocessed_data, 'original', date_string + '_COOLING_temp.csv'))
    # Print data
    print('Preprocessed data: ', os.path.join(path_preprocessed_data, 'original', date_string + '_COOLING_temp.csv'))

    # Export resampled data to csv
    data_resampled = cleaned_data.resample('H').mean()
    data_resampled.to_csv(os.path.join(path_preprocessed_data, 'resampled', date_string + '_COOLING_temp_re.csv'))
    # Print data
    print('Preprocessed and resampled data: ', os.path.join(path_preprocessed_data, 'resampled', date_string +
                                                            '_COOLING_temp_re.csv'))

    # Plot results
    plt.figure(date_string + '_external_temperatures')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y\n %H:%M'))
    plt.plot(data['T_int'], label='T_int')
    plt.plot(data['T_ext'], label='T_ext')
    plt.plot(data['T_air'], label='T_air')
    plt.xlabel('Time [hh:mm]')
    plt.ylabel('Temperature [°C]')
    plt.grid()
    plt.legend()
    plt.show()


for item in dates:
    preprocess_chiller_data(item)
