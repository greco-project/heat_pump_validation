import os
import pandas as pd
import matplotlib.pyplot as plt

# Set paths
path_file = os.path.dirname(__file__)
path_preprocessed_data = os.path.abspath(os.path.join(path_file, os.pardir, os.pardir,
                                                      'results', 'heat_pump'))


def calc_res(validation_list, simulation_data, mode):
    r"""
    calculates residual

    Parameters
    ----------

    validation_list: list, pd.Series().values.tolist()
    :param validation_list:
    :param mode:
    :param simulation_data: pd.Dataframe

    :returns
    --------
    pd.DataFrame
    Residuals from every calculated EER

    """
    residuals = []

    for quality_grade in simulation_data:
        simulation_data_list = simulation_data[quality_grade].values.tolist()
        residual = [(va_li - sim_li) for (va_li, sim_li) in zip(validation_list, simulation_data_list)]
        fill_res = pd.DataFrame({'{}'.format(quality_grade): residual})
        residuals.append(fill_res)
    residuals = pd.concat(residuals, axis=1, names=['Res_0,{}'.format(quality_grade.split('_')[1])])
    save = True
    if save is True:
        if mode == 'data_resampled':
            residuals.to_csv(os.path.join(path_preprocessed_data, 'resampled',
                                          'Residuals_resampled.csv'.format(quality_grade.split('_')[1])), index=False)
        elif mode == 'data_original':
            residuals.to_csv(os.path.join(path_preprocessed_data, 'original',
                                          'Residuals.csv'.format(quality_grade.split('_')[1])), index=False)

    return residuals


def plt_res_validation(residual_data, validation_series, mode):
    r"""
    Plots the residual data over the validation series

    Parameters
    ----------
    :param mode:
    :param residual_data: pd.DataFrame
    :param validation_series: pd.Series

    :return:
    -------

    graph
    """

    residual_data_list = list(residual_data)
    for res_name in residual_data_list:
        plt.figure()
        if mode == 'data_resampled':
            plt.xlim(0, 6)
            plt.ylim(-10, 10)
        elif mode == 'data_original':
            plt.xlim(0, 12)
            plt.ylim(-20, 20)
        plt.xlabel('{}'.format(res_name.split('_')[0]))
        plt.ylabel('Residual')
        plt.plot(validation_series, residual_data[res_name],
                 marker='+', color='green', linestyle='',
                 label='QG 0,{}'.format(res_name.split('_')[1]))
        plt.plot([0, 20], [0, 0], color='red')
        plt.legend()
        if mode == 'data_resampled':
            plt.savefig(os.path.join(path_preprocessed_data, 'resampled', 'figures',
                                     'validation_series_marker_+_{}_v2.png'.format(res_name.split('_')[1])))
        elif mode == 'data_original':
            plt.savefig(os.path.join(path_preprocessed_data, 'original', 'figures',
                                     'validation_series_marker_+_{}_v2.png'.format(res_name.split('_')[1])))
        # plt.()
        #plt.close()


    return res_name


# Plots residual series over temphub
def plt_res_temphub(residual_data, temphub, mode):
    r"""
    Plots the residual data over the temphub
    Parameters
    ----------

    :param residual_data: pd.DataFrame
    :param temphub: pd.Series

    :return:
    -------
    graph
    """

    residual_data_list = list(residual_data)
    for res_name in residual_data_list:
        plt.figure()
        if mode == 'data_resampled':
            plt.xlim(-30, 10)
            plt.ylim(-10, 10)
        elif mode == 'data_original':
            plt.xlim(-40, 10)
            plt.ylim(-70, 30)
        plt.xlabel('Temphub')
        plt.ylabel('Residual')
        plt.plot(temphub, residual_data[res_name], marker='o',
                 linestyle='', label='QG 0,{}'.format(res_name.split('_')[1]))
        plt.plot([-40, 10], [0, 0], color='r')
        plt.legend()
        if mode == 'data_original':
            plt.savefig(os.path.join(path_preprocessed_data, 'original', 'figures',
                                     'temphub_marker_o_{}.png'.format(res_name.split('_')[1])))
        elif mode == 'data_resampled':
            plt.savefig(os.path.join(path_preprocessed_data, 'resampled', 'figures',
                                     'temphub_marker_o_{}.png'.format(res_name.split('_')[1])))
        #plt.close()
        # plt.show()

    return res_name


##################################################################
# Choose what data you want to examine:
# 1. data_original -> original data
# 2. data_resampled -> resampled data
data = 'data_resampled'
##################################################################

if data == 'data_original':
    # Read data
    try:
        data_original = pd.read_csv(os.path.join(path_preprocessed_data, 'original', 'final_data.csv'))
    except FileNotFoundError:
        raise FileNotFoundError('\nData could not be read. It may not exist yet. Please run HP_Temphub.py first.\n')
    # Plot linear regression for original data
    validation_series = data_original['COP']
    simulation_data = data_original.iloc[:, 1:11]
    residual = calc_res(simulation_data=simulation_data,
                        validation_list=validation_series.values.tolist(),
                        mode=data)
    plt_res_validation(residual_data=residual,
                       validation_series=validation_series,
                       mode=data)
    plt_res_temphub(residual_data=residual, temphub=data_original['Temphub'], mode='data_original')

elif data == 'data_resampled':
    # Read data
    try:
        data_resampled = pd.read_csv(os.path.join(path_preprocessed_data, 'resampled', 'final_data_resampled.csv'))
    except FileNotFoundError:
        raise FileNotFoundError('\nData could not be read. It may not exist yet. Please run HP_Temphub.py first.\n')
    # Plot linear regression for sampled data
    validation_resampled_series = data_resampled['COP']
    simulation_resampled_data = data_resampled.iloc[:, 1:11]
    residual_resampled = calc_res(simulation_data=simulation_resampled_data,
                                  validation_list=validation_resampled_series.values.tolist(),
                                  mode=data)
    plt_res_validation(residual_data=residual_resampled,
                       validation_series=validation_resampled_series,
                       mode=data)
    plt_res_temphub(residual_data=residual_resampled, temphub=data_resampled['Temphub'], mode='data_resampled')
