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
    s = requests.get(url)
    if (s.status_code == 200):
        soup = BeautifulSoup(s.text)
        city = soup.findAll('div', class_='city-item')
        print(city)
        create_report('json.txt', city)
        
    else:
        print(f'No response from the site { url }')

collector(site1)