from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url_to_scrape = "https://store.steampowered.com/search/?filter=popularnew&sort_by=Released_DESC&os=win&ignore_preferences=1"

#Might need headers for some websites

delimiter = ';'

request_page = urlopen(url_to_scrape)

page_html = request_page.read()

request_page.close()

html_soup = BeautifulSoup(page_html, 'html.parser')

games = html_soup.findAll('a', class_="search_result_row")



filename = 'steam_data.csv'
f = open(filename, 'w')

headers = 'Title ; Release Date ; Recent Reviews ; All Reviews ; Price \n'

f.write(headers)

for game in games:

    game_url = game.get('href')

    request_page = urlopen(game_url)

    page_html = request_page.read()

    request_page.close()

    html_soup = BeautifulSoup(page_html, 'html.parser')

    game_reviews = html_soup.find_all('div', class_="user_reviews_summary_row")

    try:

        try:
            recent = game_reviews[0].find('span', class_="responsive_hidden").text
            recent = re.sub(r'\s+\(|\)\s+', '', recent)

            all = game_reviews[1].find('span', class_="responsive_hidden").text
            all = re.sub(r'\s+\(|\)\s+', '', all)
        except:
            all = game_reviews[0].find('span', class_="responsive_hidden").text
            all = re.sub(r'\s+\(|\)\s+', '', all)

    except:
        continue



    title = html_soup.find('div', class_="apphub_AppName").text

    date = html_soup.find('div', class_="date").text



    try:
        price = html_soup.find('div', class_="discount_original_price").text
        #price = re.sub(r'\s+\(|\)\s+', '', price)
    except:
        price = html_soup.find('div', class_="game_purchase_price price").text
        
    
    price = re.sub(r'\s+', '', price)


    f.write(title + delimiter + date + delimiter + recent + delimiter + all + delimiter + price + "\n")
    

    







f.close()