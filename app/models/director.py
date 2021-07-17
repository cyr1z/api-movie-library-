from . import db


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
