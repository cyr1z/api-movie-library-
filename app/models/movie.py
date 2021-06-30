"""
Movie, Genre and Director model classes

"""

from app.app import db

MovieGenre = db.Table(
    'MovieGenre',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'))
)

MovieDirector = db.Table(
    'MovieDirector',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id')),
    db.Column('director_id', db.Integer, db.ForeignKey('Director.id'))
)


class Genre(db.Model):
    """ Genre model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True)
    movies = db.relationship(
        'Movie',
        secondary=MovieGenre,
        backref='Genre')


class Director(db.Model):
    """ Director model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True)
    movies = db.relationship(
        'Movie',
        secondary=MovieDirector,
        backref='Director'
    )


class Country(db.Model):
    """ Country model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True)


class Movie(db.Model):
    """ Movie model """


    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    rate = db.Column(db.Integer)
    description = db.Column(db.Text)
    name = db.Column(db.String(64))
    poster_link = db.Column(db.String(128))
    released = db.Column(db.DateTime)
    year = db.Column(db.Integer)
    production = db.Column(db.String(250))
    genres = db.relationship(
        'Genre',
        secondary=MovieGenre,
        backref='Movie'
    )
    directors = db.relationship(
        'Director',
        secondary=MovieDirector,
        backref='Movie')
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship("Country", backref="movies")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="movies")

    def __repr__(self):
        return f"<Movie {self.id} {self.name}>"

    def __str__(self):
        return f"<Movie {self.id} {self.name}>"
