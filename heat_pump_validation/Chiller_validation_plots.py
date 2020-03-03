import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Calculates residuals between measured EER/COP and calculated EER/COP
def calc_res(validation_list, simulation_data):
    residuals = []

    for quality_grade in simulation_data:
        simulation_data_list = simulation_data[quality_grade].values.tolist()
        residual = [(va_li - sim_li) for (va_li, sim_li) in zip(validation_list, simulation_data_list)]
        fill_res = pd.DataFrame({'{}'.format(quality_grade): residual})
        residuals.append(fill_res)
    residuals = pd.concat(residuals, axis=1, names=['Res_{}'.format(quality_grade.split('_')[1])]) # Names wird im Dataframe nicht eingesetzt
    print(residuals)
    residuals.to_csv(r'')

    return residuals

# Plots residual series over temphub
def plt_res_temphub(residual_data, temphub):
    residual_data_list = list(residual_data)
    for res_name in residual_data_list:
        plt.figure()
        plt.xlabel('Temphub')
        plt.ylabel('Residual')
        plt.plot(temphub, residual_data[res_name], marker='o',
                 linestyle='', label='QG 0,{}'.format(res_name.split('_')[1]))
        plt.plot([-21, 26], [0, 0], color='r')
        plt.legend()
        plt.savefig(r'\temphub_marker_o_{}.png'.format(res_name.split('_')[1]))
        plt.close()

    return res_name


# Plots residual series over EER/COP
def plt_res_validation(residual_data, validation_series):
    residual_data_list = list(residual_data)
    for res_name in residual_data_list:
        plt.figure()
        plt.xlabel('COP')
        plt.ylabel('Residual')
        plt.plot(validation_series, residual_data[res_name],
                 marker='+', color='green', linestyle='',
                 label='QG {}'.format(res_name.split('_')[1]))
        plt.plot([0, 16], [0, 0], color='red')
        plt.legend()
        plt.savefig(r'\validation_series_marker_+_{}.png'.format(res_name.split('_')[1]))
        plt.close()
    return res_name


# Plots Histogram
def plt_hist(residual_data, bins):
    res_list = list(residual_data)
    for column in res_list:
        plt.figure()
        plt.title('Histogram for calculated COP with QG {}'.format(column.split('_')[1]))
        plt.xlabel('COP Range')
        plt.ylabel('Rate')
        plt.hist([residual_data[column]], bins=bins, rwidth=0.75, log=False, histtype='bar',
                 cumulative=False, label='QG {}'.format(column.split('_')[1]))

        plt.legend()
        plt.savefig(r'\Histogram_QG_{}.png'.format(column.split('_')[1]))
        plt.close()
    return res_list


if __name__ == '__main__':
    bins = [-16, -15.5, -15, -14.5, -14, -13.5, -13, -12.5, -12, -11.5, -11, -10.5, -10, -9.5, -9, -8.5, -8, -7.5, -7,
            -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
            
# concatenate same data type from two days           
    data = pd.concat([pd.read_csv(r''), pd.read_csv(r'')], axis=0, ignore_index=True)
    
    validation_list = data['COP'].values.tolist()
    simulation_data = data.iloc[:, 1:6]
    temphub= data['Temphub']
    
    residual = (calc_res(validation_list=validation_list,
                         simulation_data=simulation_data))   
    
    plt_res_temphub(residual_data=residual,
                    temphub=temphub)

    plt_res_validation(residual_data=residual,
                       validation_series=data['COP'])

    plt_hist(residual_data=residual,
             bins=bins)
