from bs4.element import Tag
import requests
from bs4 import BeautifulSoup

URL = 'https://bikez.com//motorcycles/bmw_r_1250_rs_2019.php'
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

response = requests.get(URL).text

soup2 = BeautifulSoup(response, 'lxml')
tables = soup2.find_all('table', {'class':'Grid'})

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
# else:
#     continue
print(temp_dict, '\n')