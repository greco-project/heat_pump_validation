import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r'C:\git\data\20190711\Histogram_data.csv')
EER_dif = data['Differenz']

EER_dif_list = EER_dif.tolist()


plt.figure()
plt.xlabel('EER Range')
plt.ylabel('Rate')
plt.hist([EER_dif_list], bins = [-6, -3, -2, -1, 0, 1, 1.5, 2, 2.5, 3, 4, 5], rwidth = 0.95,
         log=False, histtype='bar', cumulative=False,  label = ['EER dif'])
plt.legend()
plt.show()

