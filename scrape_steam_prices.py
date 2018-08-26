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

def steam_scrape(url, multi_url):
##### Retrieving HTML information #####

    uClient = uReq(url)
    steam_html = uClient.read()
    uClient.close()

    ##### Retrieving the first page information #####
    steam_soup = soup(steam_html, "html.parser")
    prod_containers = steam_soup.findAll('a', {'class': 'search_result_row'})

    #Find the total number of pages
    page_no_container = steam_soup.find('div', {'class': 'search_pagination_right'})
    page_indxs = [int(i) for i in page_no_container.stripped_strings if i.isdigit()==True]
    n_pages = max(page_indxs)

    #Adapt for multi pages
    for i in range(1, n_pages+1):
        uClient = uReq(multi_url+str(i))
        steam_html = uClient.read()
        uClient.close()
        steam_soup = soup(steam_html, "html.parser")
        prod_containers = steam_soup.findAll('a', {'class': 'search_result_row'})
        print('Entering page ' + str(i))
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
            if temp_price:
                orig_price = temp_price[0]
            else:
                orig_price = None
            # If there is a discount
            if len(temp_price) == 2:
                discounted_price = temp_price[1]
                discount_active = 1

            #Preparing document post
            price_dict = {"timestamp": current_time,
                    "Name": title_text,
                    "orig_price": orig_price,
                    "discount_active": discount_active,
                    "discounted_price": discounted_price
                    }
            #Output not required, function call inserts mongoDB item
            _ = prices.insert_one(price_dict).inserted_id