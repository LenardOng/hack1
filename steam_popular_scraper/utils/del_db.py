# Resets the database for easier prototyping

from pymongo import MongoClient as mC
mongo_client = mC('localhost', 27017)
db = mongo_client['game_prices']
db.steam.remove({})
print('Database deleted')
