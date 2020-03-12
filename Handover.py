import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import ast
import matplotlib.pyplot as plt
import numpy as np
import requests

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer 857ddfaa1d39a9ab79d62fb215e58c3',
}

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

suburbs = cleaned_suburbs[:471]

df = pd.read_csv('/Users/jihoon/Desktop/FINAL_YIELDS.csv')
df2 = pd.read_csv('/Users/jihoon/Desktop/FINAL_GROWTH.csv')

import folium

m1 = folium.Map([-33.8688, 151.2093],
                     tiles='Stamen Toner',
               zoom_start=11
              )
m1

m1.choropleth(
 geo_data=response1,
 data=df,
 columns=['suburbs','yields'],
 key_on='feature.properties.SSC_NAME',
 nan_fill_color='grey',
 nan_fill_opacity=0.1,
 fill_color='YlOrRd',
 fill_opacity=0.7,
 line_opacity=0.2,
 threshold_scale=[0, 0.0001, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.11]

)
folium.LayerControl().add_to(m1)

m1

m3 = folium.Map([-33.8688, 151.2093],
                     tiles='Stamen Toner',
               zoom_start=11
              )
m3

m3.choropleth(
 geo_data=response1,
 data=df2,
 columns=['suburbs','growth'],
 key_on='feature.properties.SSC_NAME',
 nan_fill_color='grey',
 nan_fill_opacity=0.1,
 fill_color='RdYlGn',
 fill_opacity=0.7,
 line_opacity=0.2,
 threshold_scale=[-1, -0.075 -0.05, -0.025, 0, 0.025, 0.05, 0.075, 1, 20]
)
folium.LayerControl().add_to(m3)

m3

result = pd.merge(df, df2, on=['suburbs'])
result

high_perf_yields = []
high_perf_suburbs = []
high_perf_growth = []
med_perf_yields = []
med_perf_suburbs = []
med_perf_growth = []

for index, row in result.iterrows():
    if row.yields >= 0.035:
        high_perf_yields.append(row.yields)
        high_perf_suburbs.append(row.suburbs)
        high_perf_growth.append(row.growth)
    elif row.yields >= 0.03 and row.yields < 0.035:
        med_perf_yields.append(row.yields)
        med_perf_suburbs.append(row.suburbs)
        med_perf_growth.append(row.growth)

high_df = pd.DataFrame(zip(high_perf_suburbs, high_perf_yields, high_perf_growth), columns=['suburbs', 'yields', 'growth'])
med_df = pd.DataFrame(zip(med_perf_suburbs, med_perf_yields, med_perf_growth), columns=['suburbs', 'yields', 'growth'])

def row_color(row):
    if row.growth < 0:
        return pd.Series('background-color: lightsalmon', row.index)
    elif row.growth == 0:
        return pd.Series('background-color: papayawhip', row.index)
    else:
        return pd.Series('background-color: lightgreen', row.index)

high_df.style.apply(row_color, axis=1)
med_df.style.apply(row_color, axis=1)

selected_suburbs = []

for index, row in result.iterrows():
    if row.yields >= 0.035 and row.growth > 0:
        selected_suburbs.append(row.suburbs)

selected_suburbs

medians = []
highs = []
lows = []

years1 = list(range(2005,2020))

pip install seaborn

import seaborn as sns

def analyse_history(suburb):
    
    medians = []
    highs = []
    lows = []
    firstq = []
    thirdq = []
    
    params1 = (
        ('q', suburb),
        ('match_ids', 'true'),
    )
    
    params2 = (
        ('aggregation_period', 'year'),
        ('month_end', 'december'),
        ('number_of_years', '15'),
    )

    response = requests.get('https://api.pricefinder.com.au/v1/suggest/suburbs', headers=headers, params=params1)
    suburb_1 = response.json()
    for item in suburb_1['matches']:
        if 'NSW' in item['suburb']['id']:
            suburb_Id = item['suburb']['id']
            
    response = requests.get(f'https://api.pricefinder.com.au/v1/suburbs/{suburb_Id}/stats/timeseries/sales/house', headers=headers, params=params2)
    timeseries = response.json()
    
    for year in timeseries['values']:
        try:
            medians.append(year['median'])
            if year['high'] - year['thirdQuartile'] < (year['thirdQuartile'] - year['firstQuartile'])*1.5:
                highs.append(year['high'])
            else:
                highs.append(year['thirdQuartile'] + 1)
            if year['firstQuartile'] - year['low'] < (year['thirdQuartile'] - year['firstQuartile'])*1.5:
                lows.append(year['low'])
            else:
                lows.append(year['firstQuartile'] - 1)
            firstq.append(year['firstQuartile'])
            thirdq.append(year['thirdQuartile'])
        except (KeyError):
            medians.append(0)
            highs.append(0)
            lows.append(0)
            firstq.append(0)
            thirdq.append(0)
    
    df3 = pd.DataFrame(zip(years1, medians, highs, lows, firstq, thirdq), columns=['years', 'medians', 'highs', 'lows', 'firstQuartile', 'thirdQuartile'])
    df4 = df3.set_index('years')
    df4.index.years = [None]
    plt.figure(figsize=(10,5))
    plt.ticklabel_format(style='plain', axis='y')
    sns.boxplot(x="years", y="value", data=pd.melt(df4.transpose()))
    plt.show()

analyse_history('Chatswood')

df3 = df2.copy(deep=True)

df_suburbs = pd.DataFrame(zip(suburbs, suburbs_map[:471]), columns=['cleaned_suburbs', 'suburbs'])

def mark_listings(suburb):
    
    lats = []
    lons = []
    addresses = []
    prices = []
    
    
    params = (
        ('date_end', 'now'),
        ('date_start', 'today-30d'),
        ('limit', '200'),
        ('property_type', 'house'),
    )
    
    params1 = (
        ('q', suburb),
        ('match_ids', 'true'),
    )

    response = requests.get('https://api.pricefinder.com.au/v1/suggest/suburbs', headers=headers, params=params1)
    suburb_1 = response.json()
    for item in suburb_1['matches']:
        if 'NSW' in item['suburb']['id']:
            suburb_Id = item['suburb']['id']

    response = requests.get(f'https://api.pricefinder.com.au/v1/suburbs/{suburb_Id}/listings', headers=headers, params=params)
    
    suburb_1 = response.json()
    for item in suburb_1["listings"]:
        lats.append(item["location"]["lat"])
        lons.append(item["location"]["lon"])
        addresses.append(item["address"]["streetAddress"])
        prices.append(item["price"]["display"])
        
    df = pd.DataFrame(zip(lats, lons, addresses, prices), columns=['lats', 'lons', 'addresses', 'prices'])
    
    m = folium.Map([lats[0], lons[0]], tiles='Stamen Toner', zoom_start=14)
        
    for row in df.iterrows():
        row_values = row[1]
        location = [row_values['lats'],row_values['lons']]
        popup = popup = '<strong>' + row_values['addresses'] + '\n' + row_values['prices'] + '</strong>'
        marker = folium.Marker(location = location, popup = popup)
        marker.add_to(m)
        
    index = df_suburbs.loc[df_suburbs['cleaned_suburbs'] == 'Eastwood'].index[0]
    suburb1 = df_suburbs['suburbs'].at[index]
        
    for row in df3.iterrows():
        df3.loc[df3.suburbs != suburb1, 'growth'] = 0
        df3.loc[df3.suburbs == suburb1, 'growth'] = 1   
        
    m.choropleth(
        geo_data=response1,
        data=df3,
        columns=['suburbs','growth'],
        key_on='feature.properties.SSC_NAME',
        nan_fill_color='grey',
        nan_fill_opacity=0.0,
        fill_color='Blues',
        fill_opacity=0.2,
        line_opacity=0.7,
    )
    folium.LayerControl().add_to(m)
        
    
    display(m)

mark_listings('Eastwood')

def get_agents(suburb):
    
    name = []
    personal_no = []
    agency = []
    agency_no = []
    
    params = (
        ('date_end', 'now'),
        ('date_start', 'today-30d'),
        ('limit', '100'),
    )
    
    params1 = (
        ('q', suburb),
        ('match_ids', 'true'),
    )

    response = requests.get('https://api.pricefinder.com.au/v1/suggest/suburbs', headers=headers, params=params1)
    suburb_1 = response.json()
    for item in suburb_1['matches']:
        if 'NSW' in item['suburb']['id']:
            suburb_Id = item['suburb']['id']


    response2 = requests.get(f'https://api.pricefinder.com.au/v1/suburbs/{suburb_Id}/listings', headers=headers, params=params)
    agents_list = response2.json()
    for item in agents_list['listings']:
        try:
            name.append(item['agents'][0]['name'])
        except (KeyError):
            name.append('NA')
        try:
            personal_no.append(item['agents'][0]['phoneNumber'])
        except (KeyError):
            personal_no.append('NA')
        try:
            agency.append(item['agencies'][0]['name'])
        except (KeyError):
            agency.append('NA')
        try:
            agency_no.append(item['agencies'][0]['phoneNumber'])
        except (KeyError):
            agency_no.append('NA')

    dfa = pd.DataFrame(zip(name, personal_no, agency, agency_no), columns=['name', 'phone', 'agency', 'agency no'])
    dfa.drop_duplicates(keep='first', inplace=True)
    return dfa

get_agents('Carlingford')

