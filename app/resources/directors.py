"""

Directors List Api

"""
from flask import request
from flask_restx import Resource
from marshmallow import ValidationError

from app.app import db
from app.models import Director
from app.schemas.directors import DirectorSchema


class DirectorListApi(Resource):
    """Directors List Api"""

    director_schema = DirectorSchema()

    def get(self, uuid=None):
        """Output a list, or a single director"""

        if not uuid:
            directors = db.session.query(Director).all()
            return self.director_schema.dump(directors, many=True), 200

        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            return {"Error": "Object was not found"}, 404

        return self.director_schema.dump(director), 200

    def post(self):
        """Adding a director"""

        try:
            director = self.director_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(director)
        db.session.commit()
        return self.director_schema.dump(director), 201


class DirectorApi(Resource):
    """Directors List Api"""

    director_schema = DirectorSchema()

    def put(self, uuid: int):
        """Changing a director"""

        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            return {"Error": "Object was not found"}, 404

        try:
            director = self.director_schema.load(
                request.json, instance=director, session=db.session
            )
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(director)
        db.session.commit()
        return self.director_schema.dump(director), 200

    @staticmethod
    def delete(uuid: int):
        """Deleting a director"""

        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            return "", 404

        db.session.delete(director)
        db.session.commit()
        return {"Success": "Deleted successfully"}, 200
