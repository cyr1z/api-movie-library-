"""
Seeds
"""
from random import randint

from faker import Faker

from app.models import Country, Director, Genre, User, Movie
import json

# Country
with open('/data/countries.json') as json_file:
    data = json.load(json_file)
    for item in data['data']:
        if Country.find_by_short(item['short']) is None:
            print(dict(item))
            Country(**dict(item)).save()

# Director
with open('/data/directors.json') as json_file:
    data = json.load(json_file)
    for item in data['data']:
        if Director.find_by_name(item['name']) is None:
            print(dict(item))
            Director(**dict(item)).save()

# Genre
with open('/data/genres.json') as json_file:
    data = json.load(json_file)
    for item in data['data']:
        if Genre.find_by_name(item['name']) is None:
            print(dict(item))
            Genre(**dict(item)).save()

# User
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

# Movie
with open('/data/movies.json') as datafile:
    lines = datafile.readlines()
    for line in lines:
        film = json.loads(line.strip())
        data = {
            'rate': film['rate'],
            'description': film["description"],
            'name': film["name"],
            'poster_link': film['poster_link'],
            'released': film['released'],
            'production': film["production"],
        }
        if Movie.find_by_name(data['name']) is None:
            print(dict(data))
            try:
                movie = Movie(**dict(data))

                country = Country.find_by_short(film['country']['short'])
                if country is not None:
                    movie.country = country

                for film_genre in film["genres"]:
                    genre = Genre.find_by_name(film_genre["name"])
                    if genre is not None:
                        movie.genres.append(genre)

                for film_director in film["directors"]:
                    director = Director.find_by_name(film_director["name"])
                    if director is not None:
                        movie.directors.append(director)

                user = User.get_random()
                print(user)
                if user.id is not None:
                    movie.user = user
                else:
                    movie.user = User.find_by_name('admin')


                movie.save()

            except:
                continue
