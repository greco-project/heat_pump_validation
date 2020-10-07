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

if data == 'data_original':
    try:
        datalogger_1 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190711_COOLING_temp.csv'),
                                   parse_dates=True, index_col=0)
        datalogger_2 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190712_COOLING_temp.csv'),
                                   parse_dates=True, index_col=0)
    except FileNotFoundError:
        print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_SP18.py first.\n')

    try:
        datalogger_3 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190115_COOLING_temp.csv'),
                                   parse_dates=True, index_col=0)
        datalogger_4 = pd.read_csv(os.path.join(path_preprocessed_data, 'original', '20190120_COOLING_temp.csv'),
                                   parse_dates=True, index_col=0)
    except FileNotFoundError:
        print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_MPPT.py first.\n')

    EER = pd.concat([datalogger_1, datalogger_2, datalogger_3, datalogger_4])
    try:
        datalogger = pd.read_csv(os.path.join(path_preprocessed_data, 'original', 'calc_eer_all_Tint_OUT.csv'),
                                 parse_dates=True, index_col=0)
    except FileNotFoundError:
        print('\nData could not be read. It may not exist yet. Please run calc_eer.py first.\n')

elif data == 'data_resampled':
    try:
        datalogger_1 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', '20190711_COOLING_temp_re.csv'),
                                   parse_dates=True, index_col=0)
        datalogger_2 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', '20190712_COOLING_temp_re.csv'),
                                   parse_dates=True, index_col=0)
    except FileNotFoundError:
        print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_SP18.py first.\n')

    try:
        datalogger_3 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', '20190115_COOLING_temp_re.csv'),
                                   parse_dates=True, index_col=0)
        datalogger_4 = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', '20190120_COOLING_temp_re.csv'),
                                   parse_dates=True, index_col=0)
    except FileNotFoundError:
        print('\nData could not be read. It may not exist yet. Please run Chiller_pre_processing_MPPT.py first.\n')

    EER = pd.concat([datalogger_1, datalogger_2, datalogger_3, datalogger_4])
    try:
        datalogger = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', 'calc_eer_all_Tint_OUT_re.csv'),
                                 parse_dates=True, index_col=0)
    except FileNotFoundError:
        print('\nData could not be read. It may not exist yet. Please run calc_eer.py first.\n')
plt_linear_regression(simulation_data=simulation_data,
                      validation_series=validation_series)