import pandas as pd
import os

from matplotlib import pyplot as plt

import validation_data_upm


path = os.path.join(
        os.path.expanduser('~'),
        'rl-institut/04_Projekte/220_GRECO/03-Projektinhalte/AP4_High_Penetration_of_Photovoltaics/T4_4_PV_heat_pumps/Data/UPM/csv')

# for file in
#     filename
#     for filename in os.listdir(
#             os.path.join(sys.path[0], file_dir))

data = validation_data_upm.read_heat_pump_data(path=path, date='20190711',
                                               mode='COOLING')
temperature_df = data[['T_ext_IN ', 'T_ext_OUT ', 'T_int_OUT ', 'Tint_IN']]
hourly_df = temperature_df.resample('5min').mean()

hourly_df.plot()
plt.ylabel('Temperatur in °C')
plt.grid()
plt.savefig('temperature_evaluation.pdf')


