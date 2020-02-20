import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

'''
simulation_data = {DataFrame}
validation_series = {Series}
    '''

def plt_linear_regression(simulation_data, validation_series):
    for sim_name in simulation_data:
        y =simulation_data[sim_name].values.reshape(-1, 1)
        x = validation_series.values.reshape(-1, 1)

        linear_regressor = LinearRegression().fit(y, x)
        plt.scatter(y, x, facecolors='none', edgecolors='green')
        plt.title('Correlation of measured COP to calculated COP')

        plt.xlim([0, 12])
        plt.ylim([0, 12])
        plt.xlabel('{} QG 0,{}'.format(sim_name.split('_')[0], sim_name.split('_')[1]))
        plt.ylabel('EER'.format(sim_name.split('_')[0]))
        #plt.plot([-1.513911, 3.922473], [-1.513911, 3.922473], color='red')
        plt.plot([0, 12], [0, 12], color='red')
        #plt.savefig(r'C:\git\data\PV_Chiller_COOLING\20190711\calc_EER_Tint_IN\Temphub_Tint_IN\Correlation_{}.png'.format(sim_name))
        plt.show()

    return linear_regressor
data = pd.concat([pd.read_csv(r'file:///C:\git\data\PV_Chiller_COOLING\20190711\calc_EER_Tint_IN\resampled_25.csv')],
                 axis=0, ignore_index=True)

validation_series = data['EER']
simulation_data= data[['EER_25']]
#simulation_data =data.iloc[:, 1:6]
plt_linear_regression(simulation_data=simulation_data,
                      validation_series=validation_series)


