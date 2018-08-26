# Resets the database for easier prototyping
stock_id='TPNL'
from pymongo import MongoClient as mC

mongo_client = mC('localhost', 27017)
db = mongo_client['stock_data']
db.dropDatabase({})
db[stock_id].remove({})
print('Database deleted')

