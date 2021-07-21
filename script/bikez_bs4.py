import requests
from bs4 import BeautifulSoup


INITIAL_URLS = ['https://bikez.com/year/2019-motorcycle-models.php',
                'https://bikez.com/year/2020-motorcycle-models.php',
                'https://bikez.com/year/2021-motorcycle-models.php',]

PRE_URL = 'https://bikez.com/'

response_html = requests.get(INITIAL_URLS[0]).text

soup = BeautifulSoup(response_html, 'lxml')
motor_list = soup.find('table', class_='zebra').find_all('tr', {'class':'odd'}) + soup.find('table', class_='zebra').find_all('tr', {'class':'even'})

i=0
for veh in motor_list:
    link = veh.find('td').find_all(href=True)
    if link == []:
        continue
    link = link[0]['href']

    if 'models' in link:
        continue

    print(link.replace('..', PRE_URL))
    if i == 50:
        break
    i += 1