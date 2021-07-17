"""
User model for storing user related data
And
Movie, Director, Country, Genre models

"""

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for storing user related data"""

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(50), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        """"""
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return f"{self.email}, {self.username} {self.first_name} {self.last_name}"

    @classmethod
    def find_by_username(cls, username):
        return User.query.filter(User.username == username).first()

    @classmethod
    def get_random(cls):
        return User.query.order_by(func.random()).first()

    @classmethod
    def find_by_email(cls, email):
        return User.query.filter(User.email == email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


MovieGenre = db.Table(
    "MovieGenre",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("Movie.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id")),
)

MovieDirector = db.Table(
    "MovieDirector",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("Movie.id")),
    db.Column("director_id", db.Integer, db.ForeignKey("Director.id")),
)


class Genre(db.Model):
    """Genre model"""

    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)

    @classmethod
    def find_by_name(cls, name):
        return Genre.query.filter(Genre.name == name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_or_create(cls, name):
        genre = Genre.find_by_name(name)
        if not genre:
            genre = Genre(name=name)
            genre.save()
        return genre


class Director(db.Model):
    """Director model"""

    __tablename__ = "Director"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)

    @classmethod
    def find_by_name(cls, name):
        return Director.query.filter(Director.name == name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_or_create(cls, name):
        director = Director.find_by_name(name)
        if not director:
            director = Director(name=name)
            director.save()
        return director


class Country(db.Model):
    """Country model"""

    __tablename__ = "Country"

    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(4), unique=True, index=True)
    name = db.Column(db.String(50), unique=True, index=True)

    @classmethod
    def find_by_short(cls, short):
        return Country.query.filter(Country.short == short).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_or_create(cls, name, short):
        short = short.upper().strip()
        country = Country.find_by_short(short)
        if not country:
            country = Country(name=name, short=short)
            country.save()
        return country


class Movie(db.Model):
    """Movie model"""

    __tablename__ = "Movie"

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer)
    description = db.Column(db.Text)
    name = db.Column(db.String(150))
    poster_link = db.Column(db.String(250))
    released = db.Column(db.DateTime)
    production = db.Column(db.String(250))
    genres = db.relationship("Genre", secondary=MovieGenre, backref="genre_movies")
    directors = db.relationship(
        "Director", secondary=MovieDirector, backref="director_movies"
    )
    country_id = db.Column(db.Integer, db.ForeignKey("Country.id"))
    country = db.relationship("Country", backref="country_movies")
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user = db.relationship("User", backref="user_movies")

    def __repr__(self):
        return f"<Movie {self.id} {self.name}>"

    def __str__(self):
        return f"{self.name} {self.year}>"

    @classmethod
    def find_by_name(cls, name):
        return Movie.query.filter(Movie.name == name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
