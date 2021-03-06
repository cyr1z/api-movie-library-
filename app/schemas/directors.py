""" Director schema """

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models.director import Director


class DirectorSchema(SQLAlchemyAutoSchema):
    """Director schema"""

    class Meta:
        model = Director
        load_instance = True
        include_fk = True

    id = auto_field()
