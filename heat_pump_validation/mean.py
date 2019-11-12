import pandas as pd


'''Narrow down the calculated EER (reasonable data)
calculated the mean of all data and compare with measured EER without 0 and NaN
'''
dataframe = pd.read_csv(r'C:\git\data\20190711\20190711_Mittelwert_EER.csv')
data = pd.read_csv(r'C:\git\data\20190711\20190711_EER_aktuell.csv')
temphub = dataframe[['Temphub']]

data_03 = data.loc[data.EER_03 >=8, 'EER_03'] = None
data_35 = data.loc[data.EER_35 >=8, 'EER_35'] = None
data_04 = data.loc[data.EER_04 >=8, 'EER_04'] = None
data_48 = data.loc[data.EER_48 >=8, 'EER_48'] = None
data_05 = data.loc[data.EER_05 >=8, 'EER_05'] = None


data_limit = data.dropna().mean(axis = 0)
print(data_limit)

