from pymongo import MongoClient as mC
#Prints all entries in the database

mongo_client = mC('localhost', 27017)
db = mongo_client['game_prices']
prices = db.steam
cursor = prices.find({})
for i in cursor:
    print(i)
