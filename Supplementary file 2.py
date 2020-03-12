# CODE HANDOVER

# I've been working on a few things: a heatmap, yield charts, and analysis of surrounding suburbs. 

# So far, the heatmap shows suburbs with higher rental income as darker red. This needs to be changed to measure yield instead of rental income for a particular year. 

# The following code is for the heatmap:

# Note: there are 494 entries in suburbs_map. 
# Note: there is a limit of 500 API calls per day per API key. If you test a lot of suburbs, you will get a response[429] error which means too many API calls.
      #to solve this, you need to change the API key used in the code in the "headers" section. 


=================================================================================================================================
=================================================================================================================================
=================================================================================================================================

import json
import requests
import pandas as pd
from pandas.io.json import json_normalize
import ast
import matplotlib.pyplot as plt
import numpy as np

url = "https://raw.githubusercontent.com/tim-massey/sydney-geojson/master/sydney.geojson"
response1 = requests.get(url).json()

i = 0
suburbs_map = []
while i < 494:
    suburbs_map.append(response1['features'][i]['properties']['SSC_NAME'])
    i += 1

cleaned_suburbs = []

for suburb in suburbs_map:
    if " (NSW)" in suburb:
        cleaned_suburbs.append(suburb.replace(' (NSW)', ''))
    else:
        cleaned_suburbs.append(suburb)

headers = {
    'accept': 'application/json',
    'X-Api-Key': 'key_c73215ad2e9816fc0f0a34c51e83af77',
}

#======================================================================

state = 'NSW'
bedrooms = '3'
propertyCategory = 'house'

d1 = {}
removed = 0

for suburb in cleaned_suburbs[0:200]:
    
    d1["price{0}".format(suburb)]=[]
    d1["rent{0}".format(suburb)]=[]
    
    suburbs_url = f'https://api.domain.com.au/v1/addressLocators?searchLevel=Suburb&suburb={suburb}&state=NSW'

    suburb_request = requests.get(suburbs_url, headers=headers)
    suburb_json = suburb_request.json()

    suburb_literal = ast.literal_eval(str(suburb_json))
    
    try: 
        suburbId = suburb_literal[0]['ids'][0]['id']
        url = f'https://api.domain.com.au/v1/suburbPerformanceStatistics?state={state}&suburbId={suburbId}&propertyCategory={propertyCategory}&chronologicalSpan=12&tPlusFrom=1&tPlusTo=12&bedrooms={bedrooms}'
        response = requests.get(url, headers=headers)
        j = response.json()
    
    except (ValueError, KeyError):
        cleaned_suburbs.remove(suburb)
        if suburb in suburbs_map:
            suburbs_map.remove(suburb)
        else:
            suburbs_map.remove(f'{suburb} (NSW)')
        removed += 1
    
    tab = ast.literal_eval(str(j['series']['seriesInfo']))
    dump = json.dumps(tab)
    loaded = json.loads(dump)
    
    for a in loaded:
        data = a['values']
        clean2 = data['medianSoldPrice']
        clean5 = data['medianRentListingPrice']
        
        d1[f'price{suburb}'].append(clean2)
        d1[f'rent{suburb}'].append(clean5)




price = {}
income = {}
yield1 = {}

for suburb in cleaned_suburbs[0:200-removed]:
    price['price{0}'.format(suburb)] = d1[f'price{suburb}']
    
    filtered_rent = [x/7*365 if x != None else x for x in d1[f'rent{suburb}']]

    income['{0}'.format(suburb)] = filtered_rent
    
    if len(income[suburb]) != 12:
        del income[suburb]
        cleaned_suburbs.remove(suburb)
        removed += 1
    
dff = pd.DataFrame([income][0])
dff




for i, val in enumerate(df8.columns.values):
    if val != suburbs_map[i]:
        dff.columns.values[i] = suburbs_map[i-removed]

dff.loc[11]




bb1 = dff.loc[11].fillna(0).astype(int) #converts missing data to 0

bb1


pip install folium


import folium

m1 = folium.Map([-33.8688, 151.2093],
                     tiles='Stamen Toner',
               zoom_start=11
              )
m1



m1.choropleth(
 geo_data=response1,
 data=bb1,
 columns=[x for x in suburbs_map[0:200-removed]],
 key_on='feature.properties.SSC_NAME',
 nan_fill_color='grey',
 nan_fill_opacity=0.1,
 fill_color='YlOrRd',
 fill_opacity=0.7,
 line_opacity=0.2,
)
folium.LayerControl().add_to(m1)

m1.save('map3.html')

# Should look like the heatmap image on desktop I saved. 


=================================================================================================================================
=================================================================================================================================
=================================================================================================================================


# The following code is for graphing the yield, rental and sale prices of houses in a suburb. 


# obtain rent and price for suburb for until 2008
# calculate yield for each year
# find trend in yield
# find trend in rent and price
# indicator for rising or falling rent or price

import json
import requests
import pandas as pd
from pandas.io.json import json_normalize
import ast
import matplotlib.pyplot as plt
import numpy as np

headers = {
    'accept': 'application/json',
    'X-Api-Key': 'key_3d3c066211acdc01611c9610e8243639',
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
    
suburbId = suburb_literal[0]['ids'][0]['id']
url = f'https://api.domain.com.au/v1/suburbPerformanceStatistics?state={state}&suburbId={suburbId}&propertyCategory={propertyCategory}&chronologicalSpan=12&tPlusFrom=1&tPlusTo=12&bedrooms={bedrooms}'
response = requests.get(url, headers=headers)
j = response.json()



tab = ast.literal_eval(str(j['series']['seriesInfo']))
dump = json.dumps(tab)
loaded = json.loads(dump)

price = []
rent = []
yield1 = []
final = [] 


for a in loaded:
    clean0 = a['year']
    data = a['values']
    clean2 = data['medianSoldPrice']
    clean5 = data['medianRentListingPrice']
        
    rent.append(clean5)
    price.append(clean2)
    final.append([clean0,clean2,clean5])




filtered_rent = [x/7*365 if x != None else x for x in rent]
i = 0
while i < 12:
    yield1.append(filtered_rent[i]/price[i])
    i += 1

# include error handling for None


df = pd.DataFrame(final, columns=['year', 'medianPrice', 'medianRent'])
df['yield'] = yield1
df

from matplotlib.pyplot import figure

y1 = df['medianPrice']
y2 = df['medianRent']
y3 = df['yield']
x = df['year']

ax1 = plt.gcf()
ax1.set_size_inches(10,5)

plt.plot(x, y1)
plt.show()




import seaborn as sns 

df.set_index(df['year'], inplace=True)

# tsplot with error bars
ax = sns.tsplot([df['highestSoldPrice'], df['lowestSoldPrice']], err_style="ci_bars", color='g')

ax.set_xticks(np.arange(0, df.shape[0]))
ax.set_xticklabels(df.index) 
ax.set_ylim(0, df.values.max()+1)
plt.show()