"""

Directors List Api

"""
from flask_login import login_required
from flask_restx import Resource, fields, Namespace

from app.api import api
from app.app import db
from app.models import Director
from app.schemas.directors import DirectorSchema
from app.utils.admin_required import admin_required

director_fields = api.model(
    "Director",
    {
        "name": fields.String,
    },
)

director_namespace = Namespace("director_namespace")


class DirectorListApi(Resource):
    """Directors List Api"""

    director_schema = DirectorSchema()

    def get(self):
        """Output a list, or a single director"""

        directors = db.session.query(Director).all()
        return self.director_schema.dump(directors, many=True), 200

    # @login_required
    # def post(self):
    #     """Adding a director"""
    #
    #     try:
    #         director = self.director_schema.load(request.json, session=db.session)
    #     except ValidationError as error:
    #         return {"Error": str(error)}, 400
    #
    #     db.session.add(director)
    #     db.session.commit()
    #     return self.director_schema.dump(director), 201


class DirectorApi(Resource):
    """Directors List Api"""

    director_schema = DirectorSchema()

    def get(self, uuid=None):
        """Output a list of directors"""

        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            return {"Error": "Object was not found"}, 404

        return self.director_schema.dump(director), 200

    # @login_required
    # @admin_required
    # def put(self, uuid: int):
    #     """Changing a director"""
    #
    #     director = db.session.query(Director).filter_by(id=uuid).first()
    #     if not director:
    #         return {"Error": "Object was not found"}, 404
    #
    #     try:
    #         director = self.director_schema.load(
    #             request.json, instance=director, session=db.session
    #         )
    #     except ValidationError as error:
    #         return {"Error": str(error)}, 400
    #
    #     db.session.add(director)
    #     db.session.commit()
    #     return self.director_schema.dump(director), 200

    @staticmethod
    @login_required
    @admin_required
    def delete(uuid: int):
        """Deleting a director"""

        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            return "", 404

        db.session.delete(director)
        db.session.commit()
        return {"Success": "Deleted successfully"}, 200
