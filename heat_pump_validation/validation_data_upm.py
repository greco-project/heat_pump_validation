import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def read_heat_pump_data(path, date, mode='COOLING'):
    r"""

    Parameters
    ----------
    path : str
        Points to the location of the csv files in the GRECO folder.
    date : str

    mode : str
        Specifies weather data from heating ('HEATING') or cooling mode
        ('COOLING') is loaded. Default: 'COOLING'. Note: Until now only cooling
        available.

    Returns
    -------
    data : pd.DataFrame

    """
    # read data
    datalogger = '{}_TempControl_{}_SP18_Datalogger.csv'.format(date, mode)
    datalogger_data = pd.read_csv(os.path.join(path, datalogger))
    tempcontrol = '{}_TempControl_{}_SP18_TempControl.csv'.format(date, mode)
    tempcontrol_data = pd.read_csv(os.path.join(path, tempcontrol)).rename(
        columns={'Time': 'clock'})
    # time to DatetimeIndex
    datalogger_data['Time'] = datalogger_data['Time'].apply(
        lambda x: ':'.join(x.split(':')[0: -1]))
    datalogger_data['Time'] = pd.to_datetime(datalogger_data['Time'])  # todo tz_localize
    tempcontrol_data['Time'] = pd.to_datetime(tempcontrol_data['Date'] + ' ' +
                                              tempcontrol_data['clock'])
    data = pd.concat([datalogger_data.set_index('Time'),
                      tempcontrol_data.set_index('Time')], axis=0, sort=True)
    return data


if __name__ == "__main__":
    path = os.path.join(
        os.path.expanduser('~'),
        'rl-institut/04_Projekte/220_GRECO/03-Projektinhalte/AP4_High_Penetration_of_Photovoltaics/T4_4_PV_heat_pumps/Data/UPM')
    data = read_heat_pump_data(path=path, date='20190712', mode='COOLING')
    data['P_AC (W)'].dropna().plot(legend=True)
    data['P_thermal_int (W)'].dropna().plot(legend=True)
    plt.show()
    print(data.head())
