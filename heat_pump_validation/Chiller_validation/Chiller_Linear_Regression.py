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
        plt.title('Correlation of calculated EER to measured EER')

        plt.xlim([0, 12])
        plt.ylim([0, 12])
        plt.xlabel('EER QG 0,{}'.format(sim_name.split('_')[1]))
        plt.ylabel('EER')
        plt.plot([0, 12], [0, 12], color='red')
        plt.savefig(r'C:\git\data\PV_Chiller_COOLING\Correlation_{}.png'.format(sim_name))
        plt.show()

    return linear_regressor


data = pd.read_csv(
    r'\\fs01\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\temperature_resampled\graph_data\calc_eer_all_Tint_OUT.csv',
    parse_dates=True, index_col=0).join(
    pd.read_csv(
        r'\\fs01\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\temperature_resampled\graph_data\COOLING_temp_re.csv',
        parse_dates=True, index_col=0))


validation_series = data['EER']
simulation_data =data.iloc[:, 0:7]
plt_linear_regression(simulation_data=simulation_data,
                      validation_series=validation_series)