""" Through table for movie many to many relations """

from . import db

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
