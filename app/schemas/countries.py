from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models import Country


class CountrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        load_instance = True
        include_fk = True

    # movies = Nested("MovieSchema", many=True, exclude=("movies",))
    id = auto_field()