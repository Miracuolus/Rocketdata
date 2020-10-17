import requests
from bs4 import BeautifulSoup
import os


site1 = 'https://www.mebelshara.ru/contacts'
site2 = 'https://www.tui.ru/offices/'


def create_report(file_name, value):
    os.makedirs('.\\json\\', exist_ok=True)
    folder_logs = os.path.abspath('.\\json\\' + file_name)
    with open(os.path.abspath(folder_logs), 'w') as fl:
        for i in value:
            fl.write(str(i))
        fl.write('\n')
    return fl


def collector(url):
    new_data = []
    s = requests.get(url)
    if (s.status_code == 200):
        soup = BeautifulSoup(s.text)
        group = soup.findAll('div', {'class': 'city-item'})
        #print(city)
        create_report('json.txt', group)
        for item in group:

            # getting movie_id
            city = item.find('div', {'class': 'expand-block-header js-ex-btn'}).find('h4').text
            print(city)
            shop_name = item.find('div', {'class': 'shop-name'}).text
            print(shop_name)
            address = item.find('div', {'class': 'shop-address'}).text
            print(address)
            phone = item.find('div', {'class': 'shop-phone'}).text
            print(phone)
            working_time = item.find('div', {'class': 'shop-weekends'}).text
            print(working_time)
            working_days = item.find('div', {'class': 'shop-work-time'}).text
            print(working_days)
            
            latitude = str(item).partition('data-shop-latitude="')
            print(latitude[2].split('" ')[0])
            longitude = str(item).partition('data-shop-longitude="')
            print(longitude[2].split('" ')[0])
            
    else:
        print(f'No response from the site { url }')

collector(site1)