from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from app.models import Genre


class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        include_fk = True

    movies = Nested("MovieSchema", many=True, exclude=("movies",))
