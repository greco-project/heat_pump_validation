"""
Example on how to use the 'calc_cops' function to get the
COPs of a compression chiller.

We use the ambient air as heat sink (high temperature reservoir). The input is
a list to show how the function can be applied on several time steps. The
output is a list as well and may serve as input (conversion_factor) for a
oemof.solph.transformer.
"""

import compression_heatpumps_and_chillers as cmpr_hp_chiller
import pandas as pd
import os

datalogger = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                      'data/20190711_TempControl_COOLING_SP18_Datalogger.csv'))
datalogger.set_index('Time', inplace=True)
data_t_high = datalogger['T_ext_IN'].loc['07/11/2019 09:32:59:415' : '07/11/2019 14:18:26:885']
data_t_low = datalogger['Tint_IN'].loc['07/11/2019 09:32:59:415' : '07/11/2019 14:18:26:885']

data_t_high_list = data_t_high.values.tolist()
data_t_low_list = data_t_low.values.tolist()

eer_df = pd.DataFrame()
for qg in [0.2, 0.3, 0.35, 0.4, 0.45, 0.5]:
    cops_chiller = cmpr_hp_chiller.calc_cops(t_high= data_t_high_list,
                                             t_low= data_t_low_list,
                                             quality_grade=qg,
                                             mode='chiller')
    df = pd.DataFrame(cops_chiller,
                      columns=['EER_{}'.format(''.join(str(qg).split('.')))],
                      index=data_t_high.index)
    eer_df = pd.concat([eer_df, df], axis=1)

eer_df.to_csv(os.path.join(os.path.dirname(__file__), 'data/eers.csv'), decimal='.')

print("")
print("Coefficients of Performance (COP): ", *cops_chiller, sep='\n')
print("")
