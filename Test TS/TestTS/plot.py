__author__ = 'Stephanie'
import pandas as pd


#read in csv file
data = pd.read_csv("../sample file.csv", parse_dates = True , index_col = 4)
print type(data)
print data["DataValue"].values
print data.index.values





# set up plot in a panel

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()


ax1.plot(data.index.values,data["DataValue"].values, 'b-')
ax1.set_xlabel('time (s)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('exp', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')


ax2 = ax1.twinx()
ax2.plot(data.index.values,data["DataValue"].values, 'r.')
ax2.set_ylabel('sin', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()




