"""

Directors List Api

"""
from datetime import datetime

from flask_login import login_required
from flask_restx import Resource, fields
from flask_restx.reqparse import RequestParser

from app.models import db
from app.models.director import Director
from app.resources.api import api
from app.schemas.directors import DirectorSchema
from app.utils.admin_required import admin_required

director_fields = api.model("Director", {"name": fields.String})

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

        api.logger.info(f"[{datetime.now()}], directors, get, {p_args}")

        directors = Director.query.paginate(page, per_page, error_out=False).items
        return self.director_schema.dump(directors, many=True), 200


class DirectorApi(Resource):
    """Directors List Api"""

    director_schema = DirectorSchema()

    def get(self, uuid=None):
        """Output a list of directors"""
        if not str(uuid).isdigit() or int(uuid) <= 0:
            api.logger.error(
                f'[{datetime.now()}], movies, put, "id": {uuid}, '
                f'Error: "Wrong director ID'
            )
            return {"Error": "Wrong director ID"}, 404

        uuid = int(uuid)
        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            api.logger.error(
                f'[{datetime.now()}], directors, get, "id": {uuid},'
                f' Error: "Object was not found"'
            )
            return {"Error": "Object was not found"}, 404
        api.logger.info(f'[{datetime.now()}], directors, get, "id": {uuid}, Success')
        return self.director_schema.dump(director), 200

    @staticmethod
    @login_required
    @admin_required
    def delete(uuid: int):
        """Deleting a director"""

        director = db.session.query(Director).filter_by(id=uuid).first()
        if not director:
            api.logger.error(
                f'[{datetime.now()}], directors, delete, "id": {uuid}, '
                f'Error: "Object was not found"'
            )
            return "", 404

        db.session.delete(director)
        db.session.commit()
        api.logger.info(
            f'[{datetime.now()}], directors, delete, "id": {uuid},'
            f" Deleted successfully"
        )
        return {"Success": "Deleted successfully"}, 200
