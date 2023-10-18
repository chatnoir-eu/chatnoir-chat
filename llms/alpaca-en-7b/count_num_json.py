#count how many instances in json file

import json

with open('alpaca_data.json') as f:
    data = json.load(f)
    count = len(data)
    print(count)
    print(data[1])