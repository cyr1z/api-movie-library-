"""
Movie scheme

"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.movie import Movie
from app.schemas.countries import CountrySchema
from app.schemas.directors import DirectorSchema
from app.schemas.genres import GenreSchema
from app.schemas.users import UserSchema


class MovieSchema(SQLAlchemyAutoSchema):
    """Movie scheme"""

    class Meta:
        model = Movie
        exclude = ["user_id", "country_id"]
        load_instance = True
        include_fk = True
        include_relationships = True

    directors = Nested(DirectorSchema, many=True)
    genres = Nested(GenreSchema, many=True)
    country = Nested(CountrySchema, many=False)
    id = auto_field()
    user = Nested(
        UserSchema,
        many=False,
        only=["id", "username", "first_name", "last_name", "email"],
    )
