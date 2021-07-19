""" Country schema """

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models.country import Country


class CountrySchema(SQLAlchemyAutoSchema):
    """Country schema"""

    class Meta:
        model = Country
        load_instance = True
        include_fk = True

    id = auto_field()
