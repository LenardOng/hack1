# Truncates the required JSON based on keywords, highly susceptible to webpage changes

from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as uReq
import json
from datetime import datetime
from pymongo import MongoClient as mC
import pandas as pd

##### Set up information #####

mongo_client = mC('localhost', 27017)
db = mongo_client['stock_data']
df = pd.read_csv('../data/companylist.csv')

#TODO: Did not work 356, BHACWS, 373, BNTCW, 400, BVXVW

for i in range(len(df["Symbol"])):
    current_time = datetime.utcnow().timestamp()
    print('Starting iteration number '+str(i))
    stock_id = df["Symbol"][i]
    stock_db = db['stocks']
    print(stock_id)
    url = "https://finance.yahoo.com/quote/"+stock_id+"/history?period1=1377446400&period2=1535212800&interval=1d&filter=history&frequency=1d"
    uClient = uReq(url)
    html = uClient.read()
    page_soup = bsoup(html, 'lxml')
    uClient.close()
    check = True

    # Some pages do not work, around 1 in 25
    try:
        script = page_soup.findAll('script')[26]
    except:
        print('Did not work for ' + stock_id)
        check = False

    if check:
        #Truncate the string to the required JSON
        data = script.text.split('HistoricalPriceStore')[1]
        data = data.split("gmtOffset",1)[0]
        while data[0] != '[':
            data=data[1:]
        while data[len(data)-1] != ']':
            data = data[0:len(data)-1]

        price_dict = {"timestamp": current_time,
                      "Name": stock_id,
                      "stock_history": data
                      }
        # Output not required, function call inserts mongoDB item
        _ = stock_db.insert_one(price_dict).inserted_id
