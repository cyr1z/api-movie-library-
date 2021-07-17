from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.user import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ["id", "is_admin"]
        load_instance = True
        load_only = ("password",)
