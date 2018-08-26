from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
from datetime import datetime
from pymongo import MongoClient as mC

##### Set up information #####
current_time = datetime.utcnow().timestamp()
mongo_client = mC('localhost', 27017)
db = mongo_client['game_prices']
prices = db.steam

##### Retrieving HTML information #####
steam_url = 'https://store.steampowered.com/search/?filter=popularnew&sort_by=Released_DESC&os=win'
uClient = uReq(steam_url)
steam_html = uClient.read()
uClient.close()
steam_soup = soup(steam_html, "html.parser")
prod_containers = steam_soup.findAll('a', {'class': 'search_result_row'})

for container in prod_containers:
    # Reset defaults
    discounted_price = None
    discount_active = 0
    item_title = container.find('span', class_='title')
    item_cost = container.find('div', class_='discounted')
    # Store item is not discounted, use alternate HTML tag
    if item_cost == None:
        item_cost = container.find('div', class_='search_price')
    temp_price = []
    # Stripping all strings and storing all price info
    for i in item_cost.stripped_strings:
        temp_price.append(i)
    title_text = item_title.text
    orig_price = temp_price[0]

    # If there is a discount
    if len(temp_price) == 2:
        discounted_price = temp_price[1]
        discount_active = 1

    #Preparing document post
    price_dict = {"timestamp": current_time,
            "Name": title_text,
            "orig_price": discounted_price,
            "discount_active": discount_active,
            "discounted_price": discounted_price
            }
    _ = prices.insert_one(price_dict).inserted_id

