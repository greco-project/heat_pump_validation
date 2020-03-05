import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def plt_linear_regression(simulation_data, validation_series):
    r"""
    Parameters
    ----------
    :param simulation_data: pd.DataFrame
    :param validation_series: pd.Series
    :return:
    -------
    graph
    """
    for sim_name in simulation_data:
        x =simulation_data[sim_name].values.reshape(-1, 1)
        y = validation_series.values.reshape(-1, 1)

        linear_regressor = LinearRegression().fit(x, y)
        plt.scatter(x, y, facecolors='none', edgecolors='green')
        plt.title('Correlation of calculated COP to measured COP')

        plt.xlim([0, 12])
        plt.ylim([0, 12])
        plt.xlabel('COP QG 0,{}'.format(sim_name.split('_')[1]))
        plt.ylabel('COP')
        plt.plot([0, 12], [0, 12], color='red')
        plt.savefig(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\Correlation_{}.png'.format(sim_name))
        plt.close()

    return linear_regressor


data = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\final_data.csv')
data_resampled = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\final_data_resampled.csv')


validation_series = data_resampled['COP']
simulation_data =data_resampled.iloc[:, 1:9]
plt_linear_regression(simulation_data=simulation_data,
                      validation_series=validation_series)