import pandas as pd
import matplotlib.pyplot as plt

'''
transform null values to NaN in dataframe
delete NaN values in dataframe
create new dataframe without NaN or null
data_join: connects converted column EER and Temphub
plot data_join
'''
dataframe = pd.read_csv(r'C:\git\data\20190711\20190711_Mittelwert_EER.csv')
temphub = dataframe['Temphub']

dataframe.loc[dataframe.EER == 0, 'EER'] = None
data_nan = dataframe[['EER']]

data_join = pd.concat([data_nan, temphub], axis=1)
data_final = data_join.dropna()

plt.figure()
plt.xlabel('Temphub')
plt.ylabel('EER')
plt.plot(data_final['Temphub'], data_final['EER'], linestyle = '', marker = '.')
plt.legend(['Measured EER'], loc= 'upper right')
plt.savefig(r'C:\git\data\20190711\upm_eer.png')
plt.show()
