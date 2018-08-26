import scrape_steam_prices
from scrape_steam_prices import steam_scrape

scrape = 'steam'

if scrape == 'steam':
    steam_url = 'https://store.steampowered.com/search/?filter=topsellers'
    steam_multipage = 'https://store.steampowered.com/search/?filter=topsellers&page='
    steam_scrape(steam_url, steam_multipage)

print('Done')
