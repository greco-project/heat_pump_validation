import pandas as pd
import matplotlib.pyplot as plt


# Plotting the calculated EER (QG: 0,3) over the temperature (T_ext_IN-T_int_OUT) in °C


data = pd.read_csv(r'C:\git\data\20190711\20190711_EER.csv')
# Column EER
EER_data = pd.read_csv(r'C:\git\data\20190711_TempControl_COOLING_SP18_TempControl.csv')

temphub = data['Temphub']
EER_03 = data['EER_03']


EER_OG_list = EER_03.values.tolist()
temphub_list = temphub.values.tolist()

plt.figure()
plt.xlabel('Temphub')
plt.ylabel('EER')

# plot all
plt.plot(temphub_list, EER_OG_list, linestyle = '', marker = '.')
plt.legend(['QG 0,3'], loc= 'upper right')

# manually set plot, 923:4066 EER under 8
plt.plot(temphub_list[923:4066], EER_OG_list[923:4066], label = 'EER', linestyle = '', marker = '.')
plt.legend(['QG 0,3'], loc= 'upper right')
plt.show()




