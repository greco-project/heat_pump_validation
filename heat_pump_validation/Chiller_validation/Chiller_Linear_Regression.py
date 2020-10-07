import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Set paths
path_file = os.path.dirname(__file__)
path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                      'results', 'chiller'))


def plt_linear_regression(simulation_data, validation_series, mode):
    r"""
    Parameters
    ----------
    :param mode:
    :param simulation_data: pd.DataFrame
    :param validation_series: pd.Series
    :return:
    -------
    graph
    """
    for sim_name in simulation_data:
        x = simulation_data[sim_name].values.reshape(-1, 1)
        y = validation_series.values.reshape(-1, 1)

        linear_regressor = LinearRegression().fit(x, y)
        plt.scatter(x, y, facecolors='none', edgecolors='green')
        plt.title('Correlation of calculated EER to measured EER')

        plt.xlim([0, 12])
        plt.ylim([0, 12])
        plt.xlabel('EER QG 0,{}'.format(sim_name.split('_')[1]))
        plt.ylabel('EER')
        plt.plot([0, 12], [0, 12], color='red')
        if mode == 'data_resampled':
            plt.savefig(os.path.join(path_preprocessed_data, 'resampled', 'figures',
                                     'Correlation_{}.png'.format(sim_name)))
        elif mode == 'data_original':
            plt.savefig(os.path.join(path_preprocessed_data, 'original', 'figures',
                                     'Correlation_{}.png'.format(sim_name)))
        plt.show()

    return linear_regressor


##################################################################
# Choose what data you want to examine:
# 1. data_original -> original data
# 2. data_resampled -> resampled data
data = 'data_original'
##################################################################


validation_series = data['EER']
simulation_data =data.iloc[:, 0:7]
plt_linear_regression(simulation_data=simulation_data,
                      validation_series=validation_series)