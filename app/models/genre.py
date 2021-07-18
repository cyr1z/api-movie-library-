""" Genre model module """
from . import db


class Genre(db.Model):
    """Genre model"""

    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)

    @classmethod
    def find_by_name(cls, name: str):
        """ find genre by name """
        return Genre.query.filter(Genre.name == name).first()

    def save(self):
        """ save """
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_or_create(cls, name: str):
        """ get genre by name or create it """
        genre = Genre.find_by_name(name)
        if not genre:
            genre = Genre(name=name)
            genre.save()
        return genre
