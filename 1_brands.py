import pandas as pd
import requests
import json

##################### Flatten the nested JSON structure

# Load the JSON file (brands)
with open('f:\\projects\\wiki\\llm\\true\\brands.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

rows = []
for brand in data['data']:
    a = brand.get('a')
    b = brand.get('b')
    c = brand.get('c')
    for model in brand.get('e', []):
        f = model.get('f')
        g = model.get('g')
        h = model.get('h')
        for type in model.get('i', []):
            j = type.get('j')
            k = type.get('k')
            l = type.get('l')
            m = type.get('m')
            rows.append({
                'id': a, 'name': b, 'name-en': c,
                'model-id': f, 'model-name': g, 'model-name-en': h,
                'type-id': j, 'type-name': k, 'type-name-en': l, 'type-years': m
            })

df = pd.DataFrame(rows)
df.to_csv('brands_flattened.csv', index=False, encoding='utf-8')



