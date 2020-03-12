import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import ast
import matplotlib.pyplot as plt
import numpy as np

headers = {
    'accept': 'application/json',
    'X-Api-Key': 'key_c73215ad2e9816fc0f0a34c51e83af77',
}

#======================================================================

suburb = 'Epping'
state = 'NSW'
propertyCategory = 'house'
bedrooms = '3'


#======================================================================

suburbs_url = f'https://api.domain.com.au/v1/addressLocators?searchLevel=Suburb&suburb={suburb}&state=NSW'

suburb_request = requests.get(suburbs_url, headers=headers)
suburb_json = suburb_request.json()

suburb_literal = ast.literal_eval(str(suburb_json))
suburb_dumps = json.dumps(suburb_literal)

suburbId = suburb_dumps[-9:-4]

url = f'https://api.domain.com.au/v1/suburbPerformanceStatistics?state={state}&suburbId={suburbId}&propertyCategory={propertyCategory}&chronologicalSpan=12&tPlusFrom=1&tPlusTo=12&bedrooms={bedrooms}'

response = requests.get(url, headers=headers)

j1 = response.json()

tab = ast.literal_eval(str(j1['series']['seriesInfo']))
dump = json.dumps(tab)
loaded = json.loads(dump)
final = []

for a in loaded:
    clean0 = a['year']
    data = a['values']
    clean1 = data['numberSold']
    clean2 = data['medianSoldPrice']
    clean3 = data['highestSoldPrice']
    clean4 = data['lowestSoldPrice']
    clean5 = data['medianRentListingPrice']
    clean6 = data['highestRentListingPrice']
    clean7 = data['lowestRentListingPrice']
    print(clean0,clean1,clean2,clean3,clean4,clean5,clean6,clean7)
    final.append([clean0,clean1,clean2,clean3,clean4,clean5,clean6,clean7])
   
df = pd.DataFrame(final, columns=['year', 'numberSold', 'medianSoldPrice', 'highestSoldPrice', 'lowestSoldPrice', 'medianRentListingPrice', 'highestRentListingPrice', 'lowestRentListingPrice'])
df

y1 = df['highestSoldPrice']
y2 = df['lowestSoldPrice']
y3 = df['medianRentListingPrice']
y4 = df['highestRentListingPrice']
y5 = df['lowestRentListingPrice']
x = df['year']

fig, (ax1, ax2) = plt.subplots(2, sharey=False)

ax1.plot(x,y1,x,y2)
ax1.set(title=f'Highest vs Lowest Sale and Rent Prices for {suburb}', xlabel="Year", ylabel="Sale Price")

ax2.plot(x,y3,x,y4,x,y5)
ax2.set(xlabel="Year", ylabel="Rent Price")

import matplotlib.pyplot
from matplotlib.pyplot import figure

ax1 = matplotlib.pyplot.gcf()
ax1.set_size_inches(10,10)


plt.show()





for suburb in range(len(surrounding_list)):
    suburbs_url = f'https://api.domain.com.au/v1/addressLocators?searchLevel=Suburb&suburb={suburb}&state=NSW'

    suburb_request = requests.get(suburbs_url, headers=headers)
    suburb_json = suburb_request.json()

  suburb_literal = ast.literal_eval(str(suburb_json))
  suburb_dumps = json.dumps(suburb_literal)

  suburbId = suburb_dumps[-9:-4]

  url = f'https://api.domain.com.au/v1/suburbPerformanceStatistics?state={state}&suburbId={suburbId}&propertyCategory={propertyCategory}&chronologicalSpan=12&tPlusFrom=1&tPlusTo=12&bedrooms={bedrooms}'

  response = requests.get(url, headers=headers)

  j1 = response.json()

  tab = ast.literal_eval(str(j1['series']['seriesInfo']))
  dump = json.dumps(tab)
  loaded = json.loads(dump)
  final = []

  for a in loaded:
      clean0 = a['year']
      data = a['values']
      clean1 = data['numberSold']
      clean2 = data['medianSoldPrice']
      clean3 = data['highestSoldPrice']
      clean4 = data['lowestSoldPrice']
      clean5 = data['medianRentListingPrice']
      clean6 = data['highestRentListingPrice']
      clean7 = data['lowestRentListingPrice']
      print(clean0,clean1,clean2,clean3,clean4,clean5,clean6,clean7)
      final.append([clean0,clean1,clean2,clean3,clean4,clean5,clean6,clean7])
    
  df = pd.DataFrame(final, columns=['year', 'numberSold', 'medianSoldPrice', 'highestSoldPrice', 'lowestSoldPrice', 'medianRentListingPrice', 'highestRentListingPrice', 'lowestRentListingPrice'])
  df



p1 = d1['priceBeecroft']
p2 = d1['priceCarlingford']
p3 = d1['priceCheltenham']
p5 = d1['priceDundas Valley']
p4 = d1['priceEastwood']
p7 = d1['priceMarsfield']
p6 = d1['priceNorth Epping']

r1 = [(x/7)*365 for x in d1['rentBeecroft']]
r2 = [(x/7)*365 for x in d1['rentCarlingford']]

for x in d1['rentCheltenham']:
    if x == None:
        r3 = d1['rentCheltenham']
    else:
        r3 = (x/7)*365

r5 = [(x/7)*365 for x in d1['rentDundas Valley']]
r4 = [(x/7)*365 for x in d1['rentEastwood']]
r7 = [(x/7)*365 for x in d1['rentMarsfield']]
r6 = [(x/7)*365 for x in d1['rentNorth Epping']]

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

ax1.scatter(p1, r1, c='red', label='Beecroft')
ax1.scatter(p2, r2, c='blue', label='Carlingford')
ax1.scatter(p3, r3, c='orange', label='Cheltenham')
ax1.scatter(p5, r5, c='purple', label='Dundas Valley')
ax1.scatter(p4, r4, c='green', label='Eastwood')
ax1.scatter(p7, r7, c='pink', label='Marsfield')
ax1.scatter(p6, r6, c='cyan', label='North Epping')
plt.legend(loc='upper left')
plt.gcf().set_size_inches((10, 10))
plt.show()

p1 = d1['priceBeecroft']
r1 = [(x/7)*365 for x in d1['rentBeecroft']]

y1 = []
i = 0
while i < len(p1):
    y1.append(r1[i]/p1[i])
    i += 1

    
plt.scatter(p1, y1, c='red', label='Beecroft')
fig = plt.figure()
plt.show()

price_dct = {}
rent_dct = {}
temp_dct = {}
yield_dct = {}

for suburb in surrounding_list:
    price_dct[f'{suburb}'] = d1[f'price{suburb}']
    rent_dct[f'{suburb}'] = d1[f'rent{suburb}']
    temp_dct[f'{suburb}'] = d1[f'rent{suburb}']
    for values in temp_dct.values():
        for a in values:
            if a == None:
                y = None
            else:
                y = a/7*365
            print(y)
        
price_dct = {}
rent_dct = {}
temp_dct = {}
yield_dct = {}

for suburb in surrounding_list:
    price_dct[f'{suburb}'] = d1[f'price{suburb}']
    rent_dct[f'{suburb}'] = d1[f'rent{suburb}']
    temp_dct[f'{suburb}'] = d1[f'rent{suburb}']
    for values in temp_dct.values():
        yield_dct[f'{suburb}'] = values
        
        
for values in yield_dct.values():
    for i in values:
        if i == None:
            i = None
        else:
            i = i/7*365

yield_dct

==============================================================
MAke new y list automated 
error handling for None
automate the entire process for diff suburbs
create graph for every single suburb in NSW for each year

create heatmap based on yield for each year
==============================================================

