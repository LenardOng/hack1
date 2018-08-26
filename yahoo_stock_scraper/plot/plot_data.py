# Placeholder function for the future
import json
import datetime
from pymongo import MongoClient as mC
import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

stock_name = 'PIH'

mongo_client = mC('localhost', 27017)
db = mongo_client['stock_data']
ind_stock = db['stocks'].find({'Name':stock_name})
ind_data = pd.DataFrame(list(ind_stock))
ind_json = json.loads(ind_data['stock_history'][0])
dates = []
adj_close_price=[]

for i in range(len(ind_json)):
    adj_close_price.append(ind_json[i]['adjclose'])
    try:
        date = mpl.dates.date2num(datetime.datetime.utcfromtimestamp(ind_json[i]['date']))
        dates.append(date)
        #dates.append(ind_json[i]['date'])
    except:
        dates.append(0)

fig, ax = plt.subplots()
sns.lineplot(dates, adj_close_price, ax=ax)
ax.xaxis.set_major_locator(mpl.dates.YearLocator())
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y'))

ax.set_xlim([datetime.date(2014, 1, 1), datetime.date(2019, 1, 1)])
plt.minorticks_on()
plt.grid(b=True, which='major')
plt.grid(b=True, which='minor', color='#e6e6e6')
plt.xlabel('Date')
plt.ylabel('Stock price / USD')
plt.title(stock_name)
plt.show()
