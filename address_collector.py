import requests
from bs4 import BeautifulSoup
import os
import json


site1 = 'https://www.mebelshara.ru/contacts'
site2 = 'https://www.tui.ru'


def create_report(file_name, data):
    os.makedirs('.\\json\\', exist_ok=True)
    folder_logs = os.path.abspath('.\\json\\' + file_name)
    with open(os.path.abspath(folder_logs), 'w') as fl:
        json.dump(data, fl, ensure_ascii=False, sort_keys=True, indent=4)
    return fl


def load_url(url):
    r = requests.get(url)
    return r


def collector(url):
    result = []
    s = requests.get(url)
    if (s.status_code == 200):
        soup = BeautifulSoup(s.text, features="html.parser")
        group = soup.find_all('div', {'class': 'city-item'})
        for item in group:
            city = item.find('div', {'class': 'expand-block-header js-ex-btn'}).find('h4').text
            shop_names = item.find_all('div', {'class': 'shop-list-item'})
            for shop in shop_names:
                shop_name =shop.find('div', {'class': 'shop-name'}).text
                address = shop.find('div', {'class': 'shop-address'}).text
                phone = shop.find('div', {'class': 'shop-phone'}).text
                working_time = shop.find('div', {'class': 'shop-weekends'}).text
                if 'Время работы: ' in working_time:
                    working_time = str(working_time).partition('Время работы: ')
                    working_time = working_time[2]
    
                working_days = shop.find('div', {'class': 'shop-work-time'}).text
                if 'Без выходных:' in working_days:
                    working_days = working_days.split(':')[0]
                
                latitude = str(shop).partition('data-shop-latitude="')
                latitude = latitude[2].split('" ')[0]
                longitude = str(shop).partition('data-shop-longitude="')
                longitude = longitude[2].split('" ')[0]

                result.append({
                    'address': f'{ city }, { address }',
                    'latlon': [latitude, longitude],
                    'name': shop_name,
                    'phones': [phone],
                    'working_hours': [working_days, working_time]
                })
        create_report('mebelshara.json', result)  
    else:
        print(f'No response from the site { url }')

def collector2(url):
    count = 1
    valid_response = True
    api_cities = 'https://www.tui.ru/api/office/cities'
    while valid_response:
        r = requests.get(url + '/api/office/list?cityId=' + str(count))
        if (r.status_code == 200):
            print(count)
            if r.json() == []:
                break
            count += 1
        elif (r.status_code == 404):
            valid_response = False
        else:
            pass
    #print(s.json()[0])
if __name__ == "__main__":
    collector2(site2)