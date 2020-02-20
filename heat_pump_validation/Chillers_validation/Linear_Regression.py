import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

'''all_dif = alle Differenzen der gemessenen - berechneten EER
    data_EER = alle EER (gemessen, berechnet)
    '''


eer_data = pd.read_csv(r'C:\git\data\20190711\Drop_nan.csv')
validation_series = pd.read_csv(r'C:\git\data\20190711\Histogram_data_all.csv')
def plt_linear_regression(simulation_data, validation_series):
    for sim_name in simulation_data:
        x =simulation_data[sim_name].values.reshape(-1, 1)
        y = validation_series.values.reshape(-1, 1)

        linear_regressor = LinearRegression().fit(x, y)
        plt.scatter(x, y, facecolors='none', edgecolors='green')
        plt.title('Correlation of calculated EER to measured EER')

        plt.xlim([0, 12])
        plt.ylim([0, 12])
        plt.xlabel('EER QG {}'.format(sim_name.split('_')[1]))
        plt.ylabel('EER')
        plt.plot([0, 12], [0, 12], color='red')
        #plt.savefig(r'Z:\05_Temp\Stefanie\chiller_validation\20190711\Correlation\03.png')
        plt.show()

    return linear_regressor

plt_linear_regression(simulation_data=,
                      validation_series=)

