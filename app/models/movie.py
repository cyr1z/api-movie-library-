"""
Movie, Genre and Director model classes

"""

from sqlalchemy import Table, ForeignKey, Integer, Column, String, Text, \
    DateTime
from sqlalchemy.orm import relationship

from app.app import db

MovieGenre = Table(
    'MovieGenre',
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('Movie.id')),
    Column('genre_id', Integer, ForeignKey('Genre.id'))
)

MovieDirector = Table(
    'MovieDirector',
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('Movie.id')),
    Column('director_id', Integer, ForeignKey('Director.id'))
)


class Genre(db.Model):
    """ Genre model """
    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, index=True)
    movies = relationship('Movie', secondary=MovieGenre, backref='Genre')


class Director(db.Model):
    """ Director model """
    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, index=True)
    movies = relationship('Movie', secondary=MovieDirector, backref='Director')


class Country(db.Model):
    """ Country model """
    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, index=True)


class Movie(db.Model):
    """ Movie model """
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    rate = Column(Integer)
    description = Column(Text)
    name = Column(String(64))
    poster_link = Column(String(128))
    released = Column(DateTime)
    year = Column(Integer)
    production = Column(String(250))
    genres = relationship(
        'Genre',
        secondary=MovieGenre,
        backref='Movie'
    )
    directors = relationship(
        'Director',
        secondary=MovieDirector,
        backref='Movie')
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country", backref="movies")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref="movies")

    def __repr__(self):
        return f"<Movie {self.id} {self.name}>"

    def __str__(self):
        return f"<Movie {self.id} {self.name}>"
