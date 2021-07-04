from flask import request
from flask_restx import Resource
from marshmallow import ValidationError

from app.app import db
from app.models import Country
from app.schemas.countries import CountrySchema


class CountryListApi(Resource):
    country_schema = CountrySchema()

    def get(self, uuid=None):
        """Output a list, or a single country"""

        if not uuid:
            countries = db.session.query(Country).all()
            return self.country_schema.dump(countries, many=True), 200

        country = db.session.query(Country).filter_by(id=uuid).first()
        if not country:
            return {"Error": "Object was not found"}, 404

        return self.country_schema.dump(country), 200

    def post(self):
        """Adding a country"""

        try:
            country = self.country_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(country)
        db.session.commit()
        return self.country_schema.dump(country), 201

    def put(self, uuid: int):
        """Changing a country"""

        country = db.session.query(Country).filter_by(id=uuid).first()
        if not country:
            return {"Error": "Object was not found"}, 404

        try:
            country = self.country_schema.load(
                request.json, instance=country, session=db.session
            )
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(country)
        db.session.commit()
        return self.country_schema.dump(country), 200

    @staticmethod
    def delete(uuid: int):
        """Delete a country"""

        country = db.session.query(Country).filter_by(id=uuid).first()
        if not country:
            return "", 404

        db.session.delete(country)
        db.session.commit()
        return {"Success": "Deleted successfully"}, 200
