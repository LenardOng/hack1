# Placeholder function for the future
import json
import datetime
from pymongo import MongoClient as mC
import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

# Size of moving average
window = 5
stock_name = 'PIH'

mongo_client = mC('localhost', 27017)
db = mongo_client['stock_data']
ind_stock = db['stocks'].find({'Name':stock_name})
ind_data = pd.DataFrame(list(ind_stock))
ind_json = json.loads(ind_data['stock_history'][0])

#Pre-allocation
n_datapoints = 500#len(ind_json)
dates = np.empty(n_datapoints)
adj_close_price=np.empty(n_datapoints)
dates_unix = np.empty(n_datapoints)

for i in range(n_datapoints):
    adj_close_price[i] = ind_json[i]['adjclose']
    date = mpl.dates.date2num(datetime.datetime.utcfromtimestamp(ind_json[i]['date']))
    dates[i] = date
    dates_unix[i] = ind_json[i]['date']

#Padding for the linear convolution. Moving average is identical to a convolution with a box filter
filter_window = np.ones(window)/window

#Padding differs for odd/even
if window % 2 == 0:
    pad_size = int(window/2)
    padded_acp = np.pad(adj_close_price, (pad_size, pad_size - 1), 'constant',
                        constant_values=(adj_close_price[0], adj_close_price[-1]))
else:
    pad_size = int(window / 2)
    padded_acp = np.pad(adj_close_price, (pad_size, pad_size), 'constant',
                        constant_values=(adj_close_price[0], adj_close_price[-1]))

mvg_avg = np.convolve(padded_acp, filter_window, 'valid')
print(mvg_avg.shape)
fig, ax = plt.subplots()
sns.lineplot(dates, adj_close_price, ax=ax)
sns.lineplot(dates, mvg_avg, ax=ax)
ax.xaxis.set_major_locator(mpl.dates.YearLocator())
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y'))

# Graph settins
earliest_date = datetime.datetime.utcfromtimestamp(dates_unix[-1]).strftime('%Y')
latest_date = datetime.datetime.utcfromtimestamp(dates_unix[0]).strftime('%Y')
ax.set_xlim([datetime.date(int(earliest_date), 1, 1), datetime.date(int(latest_date)+1, 1, 1)])
plt.minorticks_on()
plt.grid(b=True, which='major')
plt.grid(b=True, which='minor', color='#e6e6e6')
plt.legend(['Data', str(window)+' moving average'])
plt.xlabel('Date')
plt.ylabel('Stock price / USD')
plt.title(stock_name)
plt.show()
