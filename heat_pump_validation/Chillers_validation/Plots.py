import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

eer_data = pd.read_csv(r'file:///\\SRV02\RedirectedFolders\Stefanie.Nguyen\Desktop\temperature_resampled\calc_EER_Tint_IN\calc_eer_all.csv')
'''tint_OUT
\\SRV02\RedirectedFolders\Stefanie.Nguyen\Desktop\temperature_resampled\calc_EER_Tint_OUT\calc_eer_all_Tint_OUT.csv
'''

# Calculates residuals between measured EER/COP and calculated EER/COP
def calc_res(validation_list, simulation_data):
    residuals = []

    for quality_grade in simulation_data:
        simulation_data_list = simulation_data[quality_grade].values.tolist()
        residual = [(va_li - sim_li) for (va_li, sim_li) in zip(validation_list, simulation_data_list)]
        fill_res = pd.DataFrame({'{}'.format(quality_grade): residual})
        residuals.append(fill_res)
    residuals = pd.concat(residuals, axis=1, names=['Res_0,{}'.format(quality_grade.split('_')[1])]) # Names wird im Dataframe nicht eingesetzt
    print(residuals)
    #residuals.to_csv(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\Revised\20190711_Residuals_25.csv')

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
        plt.plot([-40, 10], [0, 0], color='r')
        plt.legend()
        plt.savefig(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\Revised\temphub_marker_o_{}.png'.format(res_name.split('_')[1]))
        plt.close()

    return res_name



# Plots residual series over EER/COP
def plt_res_validation(residual_data, validation_series):
    residual_data_list = list(residual_data)
    for res_name in residual_data_list:
        plt.figure()
        plt.xlabel('{}'.format(res_name.split('_')[0]))
        plt.ylabel('Residual')
        plt.plot(validation_series, residual_data[res_name],
                 marker='+', color='green', linestyle='',
                 label='QG 0,{}'.format(res_name.split('_')[1]))
        plt.plot([0, 16], [0, 0], color='red')
        plt.legend()
        plt.savefig(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\Revised\validation_series_marker_+_{}.png'.format(res_name.split('_')[1]))
        plt.close()
    return res_name


# Plots Histogram
def plt_hist(residual_data, bins):
    res_list = list(residual_data)
    for column in res_list:
        plt.figure()
        plt.title('Histogram for calculated EER with QG 0,{}'.format(column.split('_')[1]))
        plt.xlabel('{} Range'.format(column.split('_')[0]))
        plt.ylabel('Rate')
        plt.hist([residual_data[column]], bins=bins, rwidth=0.75, log=False, histtype='bar',
                 cumulative=False, label='QG 0,{}'.format(column.split('_')[1]))

        plt.legend()
        plt.savefig(r'\\SRV02\RL-Institut\04_Projekte\220_GRECO\03-Projektinhalte\AP4_High_Penetration_of_Photovoltaics\T4_4_PV_heat_pumps\Validierung\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\Revised\Histogram_QG_{}.png'.format(column.split('_')[1]))
        plt.close()
    return res_list



if __name__ == '__main__':
    bins = range(-16, 45)
    data = pd.concat([pd.read_csv(r'file:///C:\git\data\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\revised\20190711all_data.csv'),
                      pd.read_csv(r'file:///C:\git\data\PV_Chiller_COOLING\12_11_072019\Tint_IN_Temphub_Tint_IN\revised\20190712all_data.csv')],
                 axis=0, ignore_index=True)



    validation_list = data['EER'].values.tolist()
    simulation_data = data.iloc[:, 1:6]
    temphub= data['Temphub']

    residual = (calc_res(validation_list=validation_list,
                         simulation_data=simulation_data))


    plt_res_temphub(residual_data=residual,
                    temphub=temphub)




    plt_res_validation(residual_data=residual,
                       validation_series=data['EER'])


    plt_hist(residual_data=residual, bins=bins)
