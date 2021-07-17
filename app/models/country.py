from . import db


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
