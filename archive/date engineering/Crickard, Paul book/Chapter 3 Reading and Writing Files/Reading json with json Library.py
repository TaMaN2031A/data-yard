import json

with open('data.json', 'r') as infile:
    data = json.load(infile)

print(data['records'][0])