import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

'''
simulation_data = {DataFrame}
validation_series = {Series}
    '''

def plt_linear_regression(simulation_data, validation_series):
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
        #plt.savefig(r'C:\git\data\PV_HeatPump_HEATING\calc_cop_Tint_OUT\20190301_Tint_OUT_Temphub_T_air\Correlation_{}.png'.format(sim_name))
        plt.show()

    return linear_regressor
data = pd.concat([pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\calc_cop_Tint_OUT\20190301_Tint_OUT_Temphub_T_air\20190301_all_data.csv')],
                  #pd.read_csv(r'file:///C:\git\data\20190712\calc_EER_Tint_OUT\Temphub_Tint_IN\20190712_all_data.csv')],
                 axis=0, ignore_index=True)

validation_series = data['COP']
simulation_data =data.iloc[:, 1:6]
plt_linear_regression(simulation_data=simulation_data,
                      validation_series=validation_series)


