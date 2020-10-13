import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set paths
path_file = os.path.dirname(__file__)
path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                      'results', 'heat_pump'))


def plt_hist(residual_data, bins, mode):
    r"""
    Plots histogram

    Parameters
    ----------

    :param mode:
    :param residual_data: pd.DataFrame
    :param bins: range of int

    :return:
    -------
    graph
    """
    res_list = list(residual_data)
    for column in res_list:
        plt.figure()
        #plt.ylim(0, 2100) # all data
        #plt.ylim(0, 12) # resampled
        plt.title('Histogram for calculated COP with QG 0,{}'.format(column.split('_')[1]))
        plt.xlabel('{} Range'.format(column.split('_')[0]))
        plt.ylabel('Rate')
        plt.hist([residual_data[column]], bins=bins, rwidth=0.75, log=False, histtype='bar',
                 cumulative=False, label='QG 0,{}'.format(column.split('_')[1]))

        plt.legend()
        if mode == 'data_resampled':
            plt.savefig(os.path.join(path_preprocessed_data, 'resampled', 'figures',
                                     'Histogram_QG_{}.png'.format(column.split('_')[1])))
        elif mode == 'data_original':
            plt.savefig(os.path.join(path_preprocessed_data, 'original', 'figures',
                                     'Histogram_QG_{}.png'.format(column.split('_')[1])))
        #plt.close()
        plt.show()
    return res_list


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
    plt_hist(data_original,
             bins=np.arange(-10, 10, 0.5),
             mode=data)


elif data == 'data_resampled':
    # Read data
    try:
        data_original = data_resampled = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled',
                                                                  'Residuals_resampled.csv'))
    except FileNotFoundError:
        raise FileNotFoundError('\nData could not be read. It may not exist yet. Please run HP_Residuals.py first.\n')
    # Plot histogram for sampled data
    plt_hist(data_resampled,
             bins=np.arange(-6, 6, 0.1),
             mode=data)
