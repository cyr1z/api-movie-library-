
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from app.models import Movie


class MovieSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        exclude = ['id']
        load_instance = True
        include_fk = True
    directors = Nested('DirectorSchema', many=True, exclude=('movies',))