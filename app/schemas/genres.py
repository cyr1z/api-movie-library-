from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.genre import Genre


class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        include_fk = True
