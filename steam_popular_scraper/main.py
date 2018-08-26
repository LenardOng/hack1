# Scrapes name and prices from all the pages on steam popular list

from steam_popular_scraper.scrape_steam_prices import scrape_page

scrape = 'steam'

if scrape == 'steam':
    url = 'https://store.steampowered.com/search/?filter=topsellers'
    multipage = 'https://store.steampowered.com/search/?filter=topsellers&page='


#Not functional yet
"""
if scrape == 'gog':
    url = 'https://www.gog.com/games?sort=popularity&page=1'
    multipage = 'https://www.gog.com/games?sort=popularity&page='
"""

scrape_page(scrape, url, multipage)
print('Done')
