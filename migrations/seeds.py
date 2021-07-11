from faker import Faker

from app.models import Country, Director, Genre, User
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

fake = Faker()
for _ in range(500):
    data = fake.simple_profile()
    item = {
        'email': data['mail'],
        'username': data['username'],
        'first_name': data['name'].split()[-2],
        'last_name': data['name'].split()[-1],
        'is_admin': False
    }
    if User.find_by_username(item['username']) is None \
            and User.find_by_email(item['email']) is None:
        print(dict(item))
        user = User(**dict(item))
        user.password = item['username']
        user.save()

admin = {
    'email': 'admin@gmail.com',
    'username': 'admin',
    'first_name': 'admin',
    'last_name': 'admin',
    'is_admin': True
}
if User.find_by_username(admin['username']) is None:
    print(dict(admin))
    user = User(**dict(admin))
    user.password = admin['username']
    user.save()
