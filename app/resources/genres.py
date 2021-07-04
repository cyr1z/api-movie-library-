"""
Genre List Api

"""
from flask import request
from flask_restx import Resource
from marshmallow import ValidationError

from app.app import db
from app.models import Genre
from app.schemas.genres import GenreSchema


class GenreListApi(Resource):
    """ Genre List Api """
    genre_schema = GenreSchema()

    def get(self, uuid=None):
        """Output a list, or a single genre"""

        if not uuid:
            genres = db.session.query(Genre).all()
            return self.genre_schema.dump(genres, many=True), 200

        genre = db.session.query(Genre).filter_by(uuid=uuid).first()
        if not genre:
            return {"Error": "Object was not found"}, 404

        return self.genre_schema.dump(genre), 200

    def post(self):
        """Adding a genre"""

        try:
            genre = self.genre_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"Error": str(e)}, 400

        db.session.add(genre)
        db.session.commit()
        return self.genre_schema.dump(genre), 201

    def put(self, uuid):
        """Changing a genre"""

        genre = db.session.query(Genre).filter_by(uuid=uuid).first()
        if not genre:
            return {"Error": "Object was not found"}, 404

        try:
            genre = self.genre_schema.load(
                request.json, instance=genre, session=db.session
            )
        except ValidationError as e:
            return {"Error": str(e)}, 400

        db.session.add(genre)
        db.session.commit()
        return self.genre_schema.dump(genre), 200

    def delete(self, uuid):
        """Delete a genre"""

        genre = db.session.query(Genre).filter_by(uuid=uuid).first()
        if not genre:
            return "", 404

        db.session.delete(genre)
        db.session.commit()
        return {"Success": "Deleted successfully"}, 200
