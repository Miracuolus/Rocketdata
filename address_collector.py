import requests
from bs4 import BeautifulSoup


site1 = 'https://www.mebelshara.ru/contacts'
site2 = 'https://www.tui.ru/offices/'

def collector(url):
    s = requests.get(url)
    if (s.status_code == 200):
        soup = BeautifulSoup(s.text)
        city = soup.findAll('div', class_='city-item')
        
    else:
        print(f'No response from the site { url }')

collector(site1)