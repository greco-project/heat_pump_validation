import pandas as pd
import numpy as np
import os
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


# Choose the date written in the file name you want to examine
dates = np.array(['20190711', '20190712'])


def fix_param_name(data, name, index, new_name):
    """
    This function fixes bugs in the naming of the parameters
    :param name:
    """
    try:
        data.rename(columns={name + ' ': new_name[index]}, inplace=True)
        data.rename(columns={name: new_name[index]}, inplace=True)
    except KeyError:
        print('Value ' + name + ' not in table. Please check.')


def preprocess_chiller_data(date_string):
    # Set paths
    path_file = os.path.dirname(__file__)
    path_raw_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir, 'raw_data'))
    path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                              'results', 'chiller'))

    datalogger = pd.read_csv(os.path.join(path_raw_data, date_string + '_TempControl_COOLING_SP18_Datalogger.csv'))
    tempcontrol = pd.read_csv(os.path.join(path_raw_data, date_string + '_TempControl_COOLING_SP18_TempControl.csv'))

    datalogger['Time'] = datalogger['Time'].apply(lambda x: ':'.join(x.split(':')[0:-1]))
    datalogger['Time'] = pd.to_datetime(datalogger['Time'])

    param_to_fix = ['T_ext_IN', 'Tint_IN', 'T_int_OUT']
    param_fixed = ['T_ext', 'T_int', 'T_air']

    for index, param in enumerate(param_to_fix):
        fix_param_name(datalogger, param, index, param_fixed)

    data = pd.concat([datalogger['Time'], datalogger['T_ext'], datalogger['T_int'],
                      datalogger['T_air'], tempcontrol['EER']], axis=1,
                     names=['Time', 'T_ext', 'T_int', 'T_air', 'EER']).set_index('Time')
    data_nan = data.replace(0, np.nan).dropna()

    # Export original data to csv
    data_nan.to_csv(os.path.join(path_preprocessed_data, 'original', date_string + '_COOLING_temp.csv'))
    # Print data
    print('Preprocessed data: ', os.path.join(path_preprocessed_data, 'original', date_string + '_COOLING_temp.csv'))

    # Print how much data has been cleaned
    #print('\nDate: ', date_string,
    #      '\nData points raw data: ', len(datalogger),
    #      '\nData points preprocessed: ', len(cleaned_data),
    #      '\nRelation of cleaned data to whole data: ', (len(datalogger) - len(cleaned_data)) / len(datalogger), '\n')

    # Export resampled data to csv
    data_resampled = data_nan.resample('H').mean()
    data_resampled.to_csv(os.path.join(path_preprocessed_data, 'resampled', date_string + '_COOLING_temp_re.csv'))
    # Print data
    print('Preprocessed and resampled data: ', os.path.join(path_preprocessed_data, 'resampled', date_string +
                                                            '_COOLING_temp_re.csv'))

    # Plot results
    plt.figure(date_string + '_external_temperatures')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y\n %H:%M'))
    plt.plot(data_resampled['T_int'], label='T_int')
    plt.plot(data_resampled['T_ext'], label='T_ext')
    plt.plot(data_resampled['T_air'], label='T_air')
    plt.xlabel('Time [hh:mm]')
    plt.ylabel('Temperature [°C]')
    plt.grid()
    plt.legend()
    plt.show()


for item in dates:
    preprocess_chiller_data(item)
