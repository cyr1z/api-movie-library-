""" Movie model """

from sqlalchemy import func

from . import db
from .through_tables import MovieGenre, MovieDirector


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
        """find movie by name"""
        return Movie.query.filter(Movie.name == name).first()

    @classmethod
    def min_year(cls):
        """minimum year"""
        return db.session.query(func.min(Movie.released)).scalar().year

    @classmethod
    def max_year(cls):
        """maximum tear"""
        return db.session.query(func.max(Movie.released)).scalar().year

    def save(self):
        """save"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """delete"""
        db.session.delete(self)
        db.session.commit()
