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
bedrooms = '3'
propertyCategory = 'house'

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

r0 = df['medianRentListingPrice']/7*365
p0 = df['medianSoldPrice']

plt.scatter(p0, r0)
plt.xlabel('Median Sold Price')
plt.ylabel('Median Rental Yield')
plt.show()

scatter_response = requests.get(f'https://api.domain.com.au/v1/locations/profiles/{suburbId}', headers=headers)
scatter_json = scatter_response.json()
surrounding_suburbs = scatter_json['surroundingSuburbs']
surrounding_list = []

for index in range(len(surrounding_suburbs)):
        surrounding_list.append(surrounding_suburbs[index]['name'])

surrounding_list

d1 = {}
for suburb in surrounding_list:
    d1["price{0}".format(suburb)]=[]
    d1["rent{0}".format(suburb)]=[]

for suburb in surrounding_list:
    suburbs_url = f'https://api.domain.com.au/v1/addressLocators?searchLevel=Suburb&suburb={suburb}&state=NSW'

    suburb_request = requests.get(suburbs_url, headers=headers)
    suburb_json = suburb_request.json()

    suburb_literal = ast.literal_eval(str(suburb_json))
    suburb_dumps = json.dumps(suburb_literal)

    suburbId = suburb_dumps[-9:-4]

    url = f'https://api.domain.com.au/v1/suburbPerformanceStatistics?state={state}&suburbId={suburbId}&propertyCategory={propertyCategory}&chronologicalSpan=12&tPlusFrom=1&tPlusTo=12&bedrooms={bedrooms}'

    response = requests.get(url, headers=headers)

    j = response.json()

    tab = ast.literal_eval(str(j['series']['seriesInfo']))
    dump = json.dumps(tab)
    loaded = json.loads(dump)
    final = []
    print("\n")
    print(suburb)
   
   
   
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
        d1[f'price{suburb}'].append(clean2)
        d1[f'rent{suburb}'].append(clean5)

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

y0 = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []

i = 0
while i < len(p1):
    y0.append(r0[i]/p0[i])
    y1.append(r1[i]/p1[i])
    y2.append(r2[i]/p2[i])
    y4.append(r4[i]/p4[i])
    y5.append(r5[i]/p5[i])
    y6.append(r6[i]/p6[i])
    y7.append(r7[i]/p7[i])
    if r3[i] != None and p3[i] != None:
        y3.append(r3[i]/p3[i])
    else:
        y3.append(r3[i])
        
    i += 1


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.scatter(p0, y0, c='red', label='Epping')
ax1.scatter(p1, y1, c='red', label='Beecroft')
ax1.scatter(p2, y2, c='blue', label='Carlingford')
ax1.scatter(p3, y3, c='orange', label='Cheltenham')
ax1.scatter(p5, y5, c='purple', label='Dundas Valley')
ax1.scatter(p4, y4, c='green', label='Eastwood')
ax1.scatter(p7, y7, c='pink', label='Marsfield')
ax1.scatter(p6, y6, c='cyan', label='North Epping')
plt.legend(loc='upper right')
plt.gcf().set_size_inches((10, 10))
plt.show()

years = []
for a in loaded:
    years.append(a['year'])
    
yields_df = list(zip(years, y0, y1, y2, y3, y4, y5, y6, y7))  
  
yields_df  
  
df1 = pd.DataFrame(yields_df, columns = ['years', 'Epping', 'Beecroft', 'Carlingford', 'Cheltenham', 'Dundas Valley', 'Eastwood', 'Marsfield', 'North Epping'])  
df1 

import folium

m = folium.Map([-33.8688, 151.2093], 
               tiles='Stamen Toner',
               zoom_start=11
              )
m

folium.Choropleth(
    geo_data=df,
    name='choropleth',
    data=df,
    columns=['y1'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Rental Yield'
).add_to(m)

folium.LayerControl().add_to(m)

m

df2 = pd.read_csv("australian_postcodes.csv") 
df_2 = df2.state.str.contains("NSW")
coordinates = df2[df_2]

coordinates[coordinates['locality'].str.match('MACQUARIE PARK')]

a1 = coordinates[coordinates['locality'].str.match('BEECROFT')]
a2 = coordinates[coordinates['locality'].str.match('CARLINGFORD')]
a3 = coordinates[coordinates['locality'].str.match('CHELTENHAM')]
a4 = coordinates[coordinates['locality'].str.match('DUNDAS VALLEY')]
a5 = coordinates[coordinates['locality'].str.match('EASTWOOD')]
a6 = coordinates[coordinates['locality'].str.match('MARSFIELD')]
a7 = coordinates[coordinates['locality'].str.match('NORTH EPPING')]

added = pd.concat([a1,a2,a3,a4,a5,a6,a7])
added

for index, row in added.iterrows():
  folium.Marker([row['lat'], row['long']],
              tooltip=row['locality'],              
             ).add_to(m)

m

folium.Circle(
          location=[row['lat'], row['long']],
          tooltip=row['locality'],
          radius=2000,
          fill=True,
          color='red',
          fill_color='red'
       ).add_to(m)

m


url = "https://raw.githubusercontent.com/tim-massey/sydney-geojson/master/sydney.geojson"
response = requests.get(url).json()


m1 = folium.Map([-33.8688, 151.2093],
                     tiles='Stamen Toner',
               zoom_start=11
              )
m1


m1.choropleth(
 geo_data=response,
 data=df1,
 columns=['Epping', 'Beecroft', 'Carlingford', 'Dundas Valley', 'Eastwood', 'Marsfield', 'North Epping'],
 threshold_scale=[0, 0.01, 0.02, 0.03, 0.04, 0.05],
 key_on='feature.properties.SSC_NAME',
 fill_color='YlOrBr',
 fill_opacity=0.7,
 line_opacity=0.2,
)
folium.LayerControl().add_to(m1)

m1.save('mappus16.html')

===========================================================

markers with individiual listings???


m1.choropleth(
 geo_data=response,
 data=df1.loc[0],
 columns=['Epping', 'Beecroft', 'Carlingford', 'Dundas Valley', 'Eastwood', 'Marsfield', 'North Epping'],
 key_on='feature.properties.SSC_NAME',
 nan_fill_color='grey',
 nan_fill_opacity=0.1,
 fill_color='YlOrBr',
 fill_opacity=0.7,
 line_opacity=0.2,
)
folium.LayerControl().add_to(m1)
