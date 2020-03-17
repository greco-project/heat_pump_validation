import pandas as pd
import matplotlib.pyplot as plt


# Calculates residuals between measured EER/COP and calculated EER/COP
def calc_res(validation_list, simulation_data):
    r"""
    calculates residual

    Parameters
    ----------

    validation_list: list, pd.Series().values.tolist()
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
    residuals = pd.concat(residuals, axis=1, names=['Res_0,{}'.format(quality_grade.split('_')[1])]) # Names wird im Dataframe nicht eingesetzt
    #print(residuals)
    residuals.to_csv(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\Residuals_resampled.csv'.format(quality_grade.split('_')[1]))

    return residuals

# Calculates Temphub
def temphub(t_high_series, t_low_series):
    r"""
    Calculates the temphub with t_high as heat source and t_low as Wärmesenke(?)
    Parameters
    ----------

    :param t_high_series: pd.Series
    :param t_low_series: pd.Series

    :returns
    --------

    pd.Series
    """
    t_high_list = t_high_series.values.tolist()
    t_low_list = t_low_series.values.tolist()

    temphub = [(t_l - t_h) for (t_l, t_h) in zip(t_low_list, t_high_list)]
    temphub_series = pd.Series(temphub, name='Temphub')

    return temphub_series


# Plots residual series over temphub
def plt_res_temphub(residual_data, temphub):
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
        #plt.ylim(-25, 20) # all data
        plt.ylim(-15, 9)
        plt.xlabel('Temphub')
        plt.ylabel('Residual')
        plt.plot(temphub, residual_data[res_name], marker='o',
                 linestyle='', label='QG 0,{}'.format(res_name.split('_')[1]))
        plt.plot([-10, 10], [0, 0], color='r')
        plt.legend()
        plt.savefig(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\temphub_marker_o_{}.png'.format(res_name.split('_')[1]))
        plt.close()

    return res_name



# Plots residual series over EER/COP
def plt_res_validation(residual_data, validation_series):
    r"""
    Plots the residual data over the validation series

    Parameters
    ----------
    :param residual_data: pd.DataFrame
    :param validation_series: pd.Series

    :return:
    -------

    graph
    """

    residual_data_list = list(residual_data)
    for res_name in residual_data_list:
        plt.figure()
        #plt.ylim(-20, 17) # all data
        plt.ylim(-20, 10)
        plt.xlabel('{}'.format(res_name.split('_')[0]))
        plt.ylabel('Residual')
        plt.plot(validation_series, residual_data[res_name],
                 marker='+', color='green', linestyle='',
                 label='QG 0,{}'.format(res_name.split('_')[1]))
        plt.plot([0, 20], [0, 0], color='red')
        plt.legend()
        plt.savefig(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\validation_series_marker_+_{}.png'.format(res_name.split('_')[1]))
        plt.close()
    return res_name


# Plots Histogram
def plt_hist(residual_data, bins):
    r"""
    Plots histogram

    Parameters
    ----------

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
        plt.ylim(0, 12) # resampled
        plt.title('Histogram for calculated COP with QG 0,{}'.format(column.split('_')[1]))
        plt.xlabel('{} Range'.format(column.split('_')[0]))
        plt.ylabel('Rate')
        plt.hist([residual_data[column]], bins=bins, rwidth=0.75, log=False, histtype='bar',
                 cumulative=False, label='QG 0,{}'.format(column.split('_')[1]))

        plt.legend()
        plt.savefig(r'C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\Histogram_QG_{}.png'.format(column.split('_')[1]))
        plt.close()
    return res_list



if __name__ == '__main__':
    bins = range(-16, 45)



    data = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\final_data.csv')
    data_resampled = pd.read_csv(r'file:///C:\git\data\PV_HeatPump_HEATING\01_04_032019\resampled\final_data_resampled.csv')


    temphub = data_resampled['Temphub']

    simulation_data = data_resampled.iloc[:, 1:9]
    validation_list = data_resampled['COP'].values.tolist()

    # temphub = temphub(t_high_series= data['T_ext_IN'],
    #                   t_low_series= data['T_int_IN'])



    residual = (calc_res(validation_list=validation_list,
                         simulation_data=simulation_data))


    plt_res_temphub(residual_data=residual,
                    temphub=temphub)




    plt_res_validation(residual_data=residual,
                       validation_series=data_resampled['COP'])


    plt_hist(residual_data=residual, bins=bins)
