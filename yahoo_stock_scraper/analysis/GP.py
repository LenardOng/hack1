# Placeholder function for the future
import json
import datetime
from pymongo import MongoClient as mC
import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, RBF, ConstantKernel as C

stock_name = 'PIH'

mongo_client = mC('localhost', 27017)
db = mongo_client['stock_data']
ind_stock = db['stocks'].find({'Name':stock_name})
ind_data = pd.DataFrame(list(ind_stock))
ind_json = json.loads(ind_data['stock_history'][0])

#Pre-allocation
n_datapoints = 500 #len(ind_json)
dates = np.empty(n_datapoints)
adj_close_price=np.empty(n_datapoints)
dates_unix = np.empty(n_datapoints)

for i in range(n_datapoints):
    adj_close_price[i] = ind_json[i]['adjclose']
    date = mpl.dates.date2num(datetime.datetime.utcfromtimestamp(ind_json[i]['date']))
    dates[i] = date
    dates_unix[i] = ind_json[i]['date']

n_regression = 5000
x_unix = np.linspace(dates_unix[0]+2000000, dates_unix[-1]-2000000, n_regression)
kernel = C(1e-10) + Matern(length_scale=1) + RBF(length_scale=3)
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
gp.fit(np.reshape(dates_unix, (len(dates_unix), 1)), np.reshape(adj_close_price, (len(adj_close_price), 1)))
y_plot, sigma_plot = gp.predict(np.reshape(x_unix, (len(x_unix), 1)), return_std=True)
x_plot = np.empty(n_regression)
y_plot = y_plot.flatten()

for i in range(n_regression):
    x_plot[i] = mpl.dates.date2num(datetime.datetime.utcfromtimestamp(x_unix[i]))

print(x_plot.shape)
print(y_plot.shape)
fig, ax = plt.subplots()
sns.lineplot(dates, adj_close_price, ax=ax)
sns.lineplot(x_plot, y_plot, ax=ax)
plt.fill_between(x_plot, y_plot-2*sigma_plot, y_plot+2*sigma_plot, color='b', alpha=0.2)

ax.xaxis.set_major_locator(mpl.dates.YearLocator())
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y'))

# Graph settins
earliest_date = datetime.datetime.utcfromtimestamp(dates_unix[-1]).strftime('%Y')
latest_date = datetime.datetime.utcfromtimestamp(dates_unix[0]).strftime('%Y')
ax.set_xlim([datetime.date(int(earliest_date), 1, 1), datetime.date(int(latest_date)+1, 1, 1)])
plt.minorticks_on()
plt.grid(b=True, which='major')
plt.grid(b=True, which='minor', color='#e6e6e6')
plt.legend(['Data', 'Gaussian Process', 'Uncertainty Bounds'])
plt.xlabel('Date')
plt.ylabel('Stock price / USD')
plt.title(stock_name)
plt.show()
