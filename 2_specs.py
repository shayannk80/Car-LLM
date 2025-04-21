import pandas as pd
import requests
import json

# Load the flattened CSV file
df = pd.read_csv('test.csv', encoding='utf-8')
print(df.head())  # Inspect the first few rows

# Collect updates in a temporary structure
updates = []

for index, row in df.iterrows():
    car_type_id = int(row['type-id'])
    url = f"https://wikishop.co/api/v2/wiki/public/carTypes/{car_type_id}/specs/"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            specs_data = response.json()
            specs = specs_data.get('data', {}).get('specs', [])
            for spec in specs:
                items = spec.get('items', [])
                for item in items:
                    if isinstance(item, dict) and 'key' in item:
                        updates.append({'index': index, 'key': item['key'], 'value': item.get('value', None)})
        else:
            print(f"Failed to fetch data for type-id {car_type_id}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for type-id {car_type_id}: {e}")

# Apply updates to the DataFrame
for update in updates:
    df.at[update['index'], update['key']] = update['value']

# Save the updated DataFrame
df.to_csv('brands_flattened_complete.csv', index=False, encoding='utf-8')