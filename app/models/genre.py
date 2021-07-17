from . import db


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
