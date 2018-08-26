from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
#import pymongo as md

steam_url = 'https://store.steampowered.com/search/?filter=popularnew&sort_by=Released_DESC&os=win'
uClient = uReq(steam_url)
steam_html = uClient.read()
uClient.close()

steam_soup = soup(steam_html, "html.parser")
prod_containers = steam_soup.findAll('a', {'class': 'search_result_row'})

for container in prod_containers:
    item_title = container.find('span', class_='title')
    item_cost = container.find('div', class_='discounted')
    if item_cost == None: #Store item is not discounted
        item_cost = container.find('div', class_='search_price')
    temp_price = []
    for i in item_cost.stripped_strings:
        temp_price.append(i)
    title_text = item_title.text

    if len(temp_price) == 2:
        orig_price = temp_price[0]
        discounted_price = temp_price[1]
        print(title_text, ', Original price:', discounted_price, ', Discounted price:', orig_price)
    else:
        orig_price = temp_price[0]
        print(title_text, ', Original price:', orig_price)

