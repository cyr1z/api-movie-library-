from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Country


class CountrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        load_instance = True
        include_fk = True

    id = auto_field()
