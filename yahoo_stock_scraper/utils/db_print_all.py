from pymongo import MongoClient as mC
#Prints all entries in the database
stock_id='TURN'
mongo_client = mC('localhost', 27017)
db = mongo_client['stock_data']
prices = db[stock_id]
cursor = prices.find({})

print(db.list_collection_names())

for i in cursor:
    print(i)
