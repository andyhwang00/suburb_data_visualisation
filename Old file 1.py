price_dct = {}
rent_dct = {}
yield_dct = {}

for suburb in surrounding_list:
    price_dct[f'{suburb}'] = d1[f'price{suburb}']
    rent_dct[f'{suburb}'] = d1[f'rent{suburb}']
    
for suburb in rent_dct:
    for value in rent_dct.values():
        for x in value:
            if x == None:
                yield_dct[f'{suburb}'].append(x)
            else:
                yield_dct[f'{suburb}'] = rent_dct[f'{suburb}']

for x in value:
            if x == None:
                yield_dct[f'{suburb}'].append(x)
            else:
                yield_dct[f'{suburb}'].append(x)

