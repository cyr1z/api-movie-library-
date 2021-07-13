""" User List Api """

from flask import request
from flask_restx import Resource
from marshmallow import ValidationError


from app.models import User, db
from app.schemas.users import UserSchema


class UserListApi(Resource):
    """User List Api"""

    user_schema = UserSchema()

    def get(self, uuid=None):
        """Output a list, or a single user"""

        if not uuid:
            users = db.session.query(User).all()
            return self.user_schema.dump(users, many=True), 200

        user = db.session.query(User).filter_by(id=uuid).first()
        if not user:
            return {"Error": "Object was not found"}, 404

        return self.user_schema.dump(user), 200

    def post(self):
        """Adding a user"""

        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(user)
        db.session.commit()
        return self.user_schema.dump(user), 201

    def put(self, uuid: int):
        """Changing a user"""

        user = db.session.query(User).filter_by(id=uuid).first()
        if not user:
            return {"Error": "Object was not found"}, 404

        try:
            user = self.user_schema.load(
                request.json, instance=user, session=db.session
            )
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(user)
        db.session.commit()
        return self.user_schema.dump(user), 200

    @staticmethod
    def delete(uuid: int):
        """Delete a user"""

        user = db.session.query(User).filter_by(id=uuid).first()
        if not user:
            return "", 404

        db.session.delete(user)
        db.session.commit()
        return {"Success": "Deleted successfully"}, 200
