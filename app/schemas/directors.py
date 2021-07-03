from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from app.models import Director


class DirectorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        load_instance = True
        include_fk = True
    movies = Nested('MovieSchema', many=True, exclude=('movies',))
