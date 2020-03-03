import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

'''
simulation_data = {DataFrame}
validation_series = {Series}
    '''

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
        plt.xlabel('COP QG 0,{}'.format(sim_name.split('_')[1]))
        plt.ylabel('COP')
        plt.plot([0, 12], [0, 12], color='red')
        plt.savefig(r'C:\git\data\temperature_resampled\calc_EER_Tint_OUT\Correlation_{}.png'.format(sim_name))
        plt.show()

    return linear_regressor
#data = pd.concat([pd.read_csv(r')],
                  #pd.read_csv(r')], axis=0, ignore_index=True)
data = pd.read_csv(r'file:///C:\git\data\temperature_resampled\calc_EER_Tint_OUT\calc_eer_all_Tint_OUT.csv').join(
    pd.read_csv(r'C:\git\data\temperature_resampled\COOLING_temp_re.csv'))


validation_series = data['EER']
simulation_data =data.iloc[:, 0:6]
plt_linear_regression(simulation_data=simulation_data,
                      validation_series=validation_series)


