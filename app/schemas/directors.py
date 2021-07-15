from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models import Director

# from app.schemas.movies import MovieSchema


class DirectorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        load_instance = True
        include_fk = True

    # movies = Nested("MovieSchema", many=True, exclude=("directors",))
    id = auto_field()
