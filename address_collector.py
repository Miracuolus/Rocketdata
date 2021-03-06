import requests
from bs4 import BeautifulSoup
import os
import json


site1 = 'https://www.mebelshara.ru/contacts'
site2 = 'https://www.tui.ru'
create_folder = '.\\json\\'


def folder(file_name):
    os.makedirs(create_folder, exist_ok=True)
    folder_logs = os.path.abspath(create_folder + file_name)
    return folder_logs


def create_report(file_name, data):
    folder_logs = folder(file_name)
    with open(os.path.abspath(folder_logs), 'w', encoding='utf-8') as fl:
        json_str = json.dumps(data, ensure_ascii=False,
                              sort_keys=True, indent=4)
        fl.write(json_str)
    return fl


def collector_mebelshara(url, debug=False):
    file_name = 'mebelshara.json'
    if debug:
        print(f'Start parsing site { url }...')
    result = []
    try:
        s = requests.get(url)
    except requests.exceptions.ConnectionError:
        print(f'No response from the site { url }')
        return
    if (s.status_code == 200):
        soup = BeautifulSoup(s.text, features="html.parser")
        group = soup.find_all('div', {'class': 'city-item'})
        for item in group:
            city = item.find(
                'div', {'class': 'expand-block-header js-ex-btn'}).find('h4').text
            shop_names = item.find_all('div', {'class': 'shop-list-item'})
            for shop in shop_names:
                shop_name = shop.find('div', {'class': 'shop-name'}).text
                address = shop.find('div', {'class': 'shop-address'}).text
                phone = shop.find('div', {'class': 'shop-phone'}).text
                working_time = shop.find(
                    'div', {'class': 'shop-weekends'}).text
                if 'Время работы: ' in working_time:
                    working_time = str(working_time).partition(
                        'Время работы: ')
                    working_time = working_time[2]
                working_days = shop.find(
                    'div', {'class': 'shop-work-time'}).text
                if 'Без выходных:' in working_days:
                    working_days = working_days.split(':')[0]
                latitude = str(shop).partition('data-shop-latitude="')
                latitude = float(latitude[2].split('" ')[0])
                longitude = str(shop).partition('data-shop-longitude="')
                longitude = float(longitude[2].split('" ')[0])

                result.append({
                    'address': f'{ city }, { address }',
                    'latlon': [latitude, longitude],
                    'name': shop_name,
                    'phones': [phone],
                    'working_hours': [working_days, working_time]
                })
        create_report(file_name, result)
        if debug:
            f = folder(file_name)
            print(f"The result has saved in  { f }")
    else:
        print(f'No response from the site { url }')


def tui_cities(api_cities):
    r = requests.get(api_cities)
    all_cities = r.json()
    id_city = []
    for city in all_cities:
        id_city.append(city['cityId'])
    return id_city


def collector_tui(url, debug=False):
    file_name = 'tui.json'
    api_cities = 'https://www.tui.ru/api/office/cities'
    if debug:
        print(f'Start parsing site { url }...')
    try:
        id_city = tui_cities(api_cities)
    except requests.exceptions.ConnectionError:
        print(f'No response from the site { api_cities }')
        return
    result = []
    for i in id_city:
        try:
            r = requests.get(url + '/api/office/list?cityId=' + str(i))
        except requests.exceptions.ConnectionError:
            print(f'No response from the site { url }')
            return
        if (r.status_code == 200):
            city_office = r.json()
            if city_office != []:
                for i in city_office:
                    phones = []
                    for p in i['phones']:
                        phones.append(p['phone'].strip())
                    message = ''
                    hours = []
                    for key in i["hoursOfOperation"].keys():
                        if key == 'workdays' and i['hoursOfOperation']['workdays'].get('startStr'):
                            message = f"пн - пт { i['hoursOfOperation']['workdays']['startStr'] } - { i['hoursOfOperation']['workdays']['endStr'] }"
                            hours.append(message)
                        elif key == 'saturday' and i['hoursOfOperation']['saturday'].get('startStr'):
                            message = f"сб { i['hoursOfOperation']['saturday']['startStr'] } - { i['hoursOfOperation']['saturday']['endStr'] }"
                            hours.append(message)
                        elif key == 'sunday' and i['hoursOfOperation']['sunday'].get('startStr'):
                            message = f"вс { i['hoursOfOperation']['sunday']['startStr'] } - { i['hoursOfOperation']['sunday']['endStr'] }"
                            hours.append(message)
                    result.append({
                        'address': i['address'],
                        'latlon': [i['latitude'], i['longitude']],
                        'name': i['name'],
                        'phones': phones,
                        'working_hours': hours
                    })
        elif (r.status_code == 404):
            print(f'No response from the site { url }')
        else:
            pass
    create_report(file_name, result)
    if debug:
        f = folder(file_name)
        print(f"The result has saved in  { f }")


if __name__ == "__main__":
    collector_mebelshara(site1, debug=True)
    collector_tui(site2, debug=True)
