from os import name
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

link = 'https://www.talabat.com/uae/restaurant/650400/souperior--hearty-soups-jumeirah-lakes-tower--jlt?aid=1308'
r = requests.get(link)
soup = BeautifulSoup(r.text, 'html.parser')

#Scraping data under script tag with id='__NEXT_DATA__'
s = soup.find('script', id='__NEXT_DATA__')

#JSON Formatting
json = json.loads(s.string)
node1 = json['props']['pageProps']['initialMenuState']['restaurant']
node2 = json['props']['pageProps']['initialMenuState']['menuData']['items']

#Creating tables for displaying necessary fields

menu = []
for i in range(len(node2)):
  menu.append(node2[i]['name'])

table = {}
table["restaurant_name"] = [node1["name"]]
table["restaurant_logo"] = [node1["logo"]]
table["latitude"] = [node1["latitude"]]
table["longitude"] = [node1["longitude"]]
table["cuisine_tags"] = [node1["cuisineString"]]
table["menu_items"] = []
table.update({"menu_items": [','.join(map(str, menu))]})

menu_table = [{} for i in range(len(node2))]
for i in range(len(node2)):
  menu_table[i]["item_name"] = [node2[i]["name"]]
  menu_table[i]["item_description"] = [node2[i]["description"]]
  menu_table[i]["item_price"] = [node2[i]["price"]]
  menu_table[i]["item_image"] = [node2[i]["originalImage"]]


#Printing tables
df1 = pd. DataFrame(data=table)
df1 = (df1. T)
print(df1)

df = pd. DataFrame(data=menu_table)
df = (df. T)
print(df)

# writing to Excel
datatoexcel = pd.ExcelWriter('Link10.xlsx')
  
# write DataFrame to excel
df1.to_excel(datatoexcel)
df.to_excel(datatoexcel, startrow=20,)
  
# save the excel
datatoexcel.save()
print('DataFrame is written to Excel File successfully.')

# Final JSON data, which connects restaurant table and menu table
final = table
final.update({"menu_items_details": menu_table})