from os import error
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

INITIAL_URLS = ['https://bikez.com/year/2019-motorcycle-models.php',
                'https://bikez.com/year/2020-motorcycle-models.php',
                'https://bikez.com/year/2021-motorcycle-models.php',
                'https://bikez.com/year/2018-motorcycle-models.php',]

FIELDS =   ['Model:',
            'Year:',
            'Displacement',
            'Engine type:',
            'Power:',
            'Compression:',
            'Bore x stroke:',
            'Valves per cylinder:',
            'Gearbox:',
            'Greenhouse gases:',
            'Wheelbase:',
            'Fuel capacity:',
            ]

PRE_URL = 'https://bikez.com'

data = list()

for main_model_url in INITIAL_URLS:
    print('Current no. of rows: ', len(data))
    print('scraping from: ', main_model_url)

    errors = 0
    response_html = requests.get(main_model_url).text

    soup = BeautifulSoup(response_html, 'lxml')
    motor_list = soup.find('table', class_='zebra').find_all('tr', {'class':'odd'}) + soup.find('table', class_='zebra').find_all('tr', {'class':'even'})

    for veh in tqdm(motor_list):
        link = veh.find('td').find_all(href=True)
        if link == []:
            continue
        link = link[0]['href']

        if 'models' in link:
            continue

        url = link.replace('..', PRE_URL)

        response = requests.get(url).text

        soup2 = BeautifulSoup(response, 'lxml')
        tables = soup2.find_all('table', {'class':'Grid'})
        try:
            for grid in tables:
                if grid.find('tr').text == 'General information':
                    table = grid
                    break

            tr_list = table.find_all('tr')
            temp_dict = dict()
            for row in tr_list:
                
                td = row.find_all('td')
                if td != []:
                    if td[0].text in FIELDS:
                        field_name = td[0].text.lower()[0:-1]
                        temp_dict[field_name] = td[1].text

            if 'greenhouse gases' in temp_dict:
                temp_dict['greenhouse gases'] = temp_dict['greenhouse gases'].split(' CO2 g/km.')[0]
            else:
                temp_dict['greenhouse gases'] = '0'

            if len(temp_dict) == 11:
                temp_dict['power'] = temp_dict['power'].split(' ')[2].replace('(','')
                temp_dict['compression'] = temp_dict['compression'].split(':')[0]
                temp_dict['bore'], temp_dict['stroke'] = temp_dict['bore x stroke'].split(' ')[0], temp_dict['bore x stroke'].split(' ')[2]
                del temp_dict['bore x stroke']
                temp_dict['wheelbase'] = temp_dict['wheelbase'].split(' mm')[0]
                temp_dict['fuel capacity'] = temp_dict['fuel capacity'].split(' litre')[0]
            else:
                continue

            data.append(temp_dict)
        except requests.exceptions.ConnectionError:
            errors += 1
            continue
    print('errors: ', errors)
    
df = pd.DataFrame(data)
df.to_csv(r'C:\Users\Chulabutrach\Documents\Coding\Projects\bingsu\datascraping\data\motor_cycle_data_2018-2021.csv', sep='|')