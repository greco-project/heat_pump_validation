import os
import pandas as pd
import numpy as np

# Set paths
path_file = os.path.dirname(__file__)
path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                      'results', 'heat_pump'))


def calc_rmse(residual_data, mode):
    rmse = pd.DataFrame()
    res_list = list(residual_data)
    for index, column in enumerate(res_list):
        rmse[column] = [np.sqrt(np.mean(residual_data[column]**2))]
    return rmse


# Arrange quality grades
quality_grades = np.arange(0.05, 0.55, 0.05)

##################################################################
# Choose what data you want to examine:
# 1. data_original -> original data
# 2. data_resampled -> resampled data
data = 'data_resampled'
##################################################################

if data == 'data_original':
    # Read data
    try:
        data_original = pd.read_csv(os.path.join(path_preprocessed_data, 'original', 'Residuals.csv'))
    except FileNotFoundError:
        raise FileNotFoundError('\nData could not be read. It may not exist yet. Please run HP_Residuals.py first.\n')
    # Plot histogram for original data
    rmse = calc_rmse(data_original, mode=data)


elif data == 'data_resampled':
    # Read data
    try:
        data_resampled = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', 'Residuals_resampled.csv'))
    except FileNotFoundError:
        raise FileNotFoundError('\nData could not be read. It may not exist yet. Please run HP_Residuals.py first.\n')
    # Plot histogram for sampled data
    rmse = calc_rmse(data_resampled, mode=data)

# Print RMSE with .T for transposed and 0th element in Dataframe with just one value
print('\nRMSE of ' + data.split('_')[1] + ' data:\n\n' + str(np.round(rmse.T[0], 3)))
