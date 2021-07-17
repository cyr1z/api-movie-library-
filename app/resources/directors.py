"""

Directors List Api

"""
from flask_login import login_required
from flask_restx import Resource, fields, Namespace
from flask_restx.reqparse import RequestParser

from app.resources.api import api
from app.models import db
from app.models.director import Director
from app.schemas.directors import DirectorSchema
from app.utils.admin_required import admin_required

director_fields = api.model(
    "Director",
    {
        "name": fields.String,
    },
)

director_namespace = Namespace("director_namespace")

pagination_parser = RequestParser()
pagination_parser.add_argument(
    "pageNumber", type=int, required=False, default=1, help="Page number"
)
pagination_parser.add_argument(
    "pageSize", type=int, required=False, default=10, help="Page size"
)


class DirectorListApi(Resource):
    """Directors List Api"""

    director_schema = DirectorSchema()

    @api.expect(pagination_parser)
    def get(self):
        """Output a list, or a single director"""

        p_args = pagination_parser.parse_args()

        page = p_args.get("pageNumber")
        per_page = p_args.get("pageSize")

        directors = Director.query.paginate(page, per_page, error_out=False).items
        return self.director_schema.dump(directors, many=True), 200


class DirectorApi(Resource):
    """Directors List Api"""

    director_schema = DirectorSchema()

    def get(self, uuid=None):
        """Output a list of directors"""

        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            return {"Error": "Object was not found"}, 404

        return self.director_schema.dump(director), 200

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
