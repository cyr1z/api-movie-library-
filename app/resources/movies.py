""" Movie List Api """

from flask import request
from flask_restx import Resource
from marshmallow import ValidationError

from app.app import db
from app.models import Movie
from app.schemas.movies import MovieSchema


class MovieListApi(Resource):
    """ Movie List Api """

    movie_schema = MovieSchema()

    def get(self, uuid=None):
        """Output a list, or a single movie"""

        if not uuid:
            movies = db.session.query(Movie).all()
            return self.movie_schema.dump(movies, many=True), 200

        movie = db.session.query(Movie).filter_by(id=uuid).first()
        if not movie:
            return {"Error": "Object was not found"}, 404

        return self.movie_schema.dump(movie), 200

    def post(self):
        """Adding a movie"""

        try:
            movie = self.movie_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(movie)
        db.session.commit()
        return self.movie_schema.dump(movie), 201

    def put(self, uuid: id):
        """Changing a movie"""

        movie = db.session.query(Movie).filter_by(id=uuid).first()
        if not movie:
            return {"Error": "Object was not found"}, 404

        try:
            movie = self.movie_schema.load(
                request.json, instance=movie, session=db.session
            )
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(movie)
        db.session.commit()
        return self.movie_schema.dump(movie), 200

    @staticmethod
    def delete(uuid: int):
        """Delete a movie"""

        movie = db.session.query(Movie).filter_by(id=uuid).first()
        if not movie:
            return "", 404

        db.session.delete(movie)
        db.session.commit()
        return {"Success": "Deleted successfully"}, 200
