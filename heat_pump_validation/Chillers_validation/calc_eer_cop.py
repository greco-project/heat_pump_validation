import pandas as pd
import numpy as np

''' 
Calculates COP or EER 
Corrections were made to avoid ZeroDivisionError'''

def calc_cops(t_high, t_low, quality_grade,
              consider_icing=False, factor_icing=None, mode=None):
    length = max([len(t_high), len(t_low)])
    if len(t_high) == 1:
        list_t_high_K = [t_high[0] + 273.15] * length
    elif len(t_high) == length:
        list_t_high_K = [t + 273.15 for t in t_high]
    if len(t_low) == 1:
        list_t_low_K = [t_low[0] + 273.15] * length
    elif len(t_low) == length:
        list_t_low_K = [t + 273.15 for t in t_low]

    if not consider_icing:
        if mode == "heat_pump":
            try:
                cops = [quality_grade * t_h / (t_h - t_l) for
                        t_h, t_l in zip(list_t_high_K, list_t_low_K)]
            except ZeroDivisionError:
                list_dif_temp = [(t_h - t_l) for t_h, t_l in zip(list_t_high_K, list_t_low_K)]
                cops_df = pd.DataFrame({'temp_dif': list_dif_temp, 'T': pd.Series(list_t_high_K)})
                cops_drop_zero = cops_df.replace(0, np.nan).dropna()
                list_t_high_new_K = cops_drop_zero['T'].tolist()
                list_dif_temp_new = cops_drop_zero['temp_dif'].tolist()
                cops = [quality_grade * (t_h / (t_dif)) for
                        t_h, t_dif in zip(list_t_high_new_K, list_dif_temp_new)]
        if mode == "chiller":
            try:
                cops = [quality_grade * t_l /(t_h - t_l) for
                    t_h, t_l in zip(list_t_high_K, list_t_low_K)]
            except ZeroDivisionError:
                list_dif_temp = [(t_h - t_l) for t_h, t_l in zip(list_t_high_K, list_t_low_K)]
                cops_df = pd.DataFrame({'temp_dif': list_dif_temp, 'T_int': pd.Series(list_t_low_K)})
                cops_drop_zero = cops_df.replace(0, np.nan).dropna()
                list_t_low_new_K = cops_drop_zero['T_int'].tolist()
                list_dif_temp_new = cops_drop_zero['temp_dif'].tolist()
                cops =[quality_grade * (t_l /(t_dif)) for
                    t_l, t_dif in zip(list_t_low_new_K, list_dif_temp_new)]


    return cops

#datalogger = pd.read_csv(r'\\SRV02\RedirectedFolders\Stefanie.Nguyen\Desktop\temperature_resampled\COOLING_temp_re.csv',
#                         encoding='unicode_escape', low_memory=False)
datalogger = pd.read_csv(r'\\SRV02\RedirectedFolders\Stefanie.Nguyen\Desktop\temperature_resampled\COOLING_temp_re.csv')

# chiller
data_t_high = datalogger['T_ext_IN']
data_t_low = datalogger['T_int_IN']


data_t_high_list = data_t_high.values.tolist()
data_t_low_list = data_t_low.values.tolist()

# cops_chiller = cmpr_hp_chiller.calc_cops(t_high= data_t_high_list,

cops_chiller = calc_cops(t_high=data_t_high_list,
                         t_low=data_t_low_list,
                         quality_grade=0.3,
                         mode="chiller")

dataseries = pd.DataFrame(cops_chiller)
print(dataseries)
dataseries.to_csv(r'\\SRV02\RedirectedFolders\Stefanie.Nguyen\Desktop\temperature_resampled\calc_EER_ Tint_IN\EER_3_3.csv', decimal='.')