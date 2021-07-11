from app.models import Country, Director, Genre
import json


with open('/data/countries.json') as json_file:
    data = json.load(json_file)
    for item in data['data']:
        if Country.find_by_short(item['short']) is None:
            print(dict(item))
            Country(**dict(item)).save()

with open('/data/directors.json') as json_file:
    data = json.load(json_file)
    for item in data['data']:
        if Director.find_by_name(item['name']) is None:
            print(dict(item))
            Director(**dict(item)).save()

with open('/data/genres.json') as json_file:
    data = json.load(json_file)
    for item in data['data']:
        if Genre.find_by_name(item['name']) is None:
            print(dict(item))
            Genre(**dict(item)).save()
