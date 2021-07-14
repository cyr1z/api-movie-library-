""" Movie List Api """

from flask import request, current_app
from flask_login import login_required, current_user
from flask_restx import Resource, fields, Namespace
from marshmallow import ValidationError

from app.api import api
from app.models import Movie, db
from app.schemas.movies import MovieSchema

movie_fields = api.model(
    "Movie",
    {
        "rate": fields.Integer,
        "description": fields.String,
        "name": fields.String,
        "poster_link": fields.Url,
        "released": fields.Date,
        "production": fields.String,
        # "genres": fields.List,
        # "directors": fields.List,
        # "country": fields.String,
    },
)

movie_namespace = Namespace("movie_namespace")


class MovieListApi(Resource):
    """Movie List Api"""

    movie_schema = MovieSchema()

    def get(self):
        """Output a list movies"""

        movies = db.session.query(Movie).all()
        return self.movie_schema.dump(movies, many=True), 200

    @login_required
    @movie_namespace.expect(movie_fields, validate=True)
    def post(self):
        """Adding a movie"""

        try:
            movie = self.movie_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(movie)
        db.session.commit()
        return self.movie_schema.dump(movie), 201


class MovieApi(Resource):
    """Movie Api"""

    movie_schema = MovieSchema()

    def get(self, uuid=None):
        """Output a single movie"""

        movie = db.session.query(Movie).filter_by(id=uuid).first()
        if not movie:
            return {"Error": "Object was not found"}, 404

        return self.movie_schema.dump(movie), 200

    @login_required
    @movie_namespace.expect(movie_fields, validate=True)
    def put(self, uuid: id):
        """Changing a movie"""

        movie = db.session.query(Movie).filter_by(id=uuid).first()
        if not movie:
            return {"Error": "Object was not found"}, 404

        if current_user.is_admin or current_user == movie.user:
            try:
                movie = self.movie_schema.load(
                    request.json, instance=movie, session=db.session
                )
            except ValidationError as error:
                return {"Error": str(error)}, 400

            db.session.add(movie)
            db.session.commit()
            return self.movie_schema.dump(movie), 200
        else:
            return current_app.login_manager.unauthorized()

    @staticmethod
    @login_required
    def delete(uuid: int):
        """Delete a movie"""

        movie = db.session.query(Movie).filter_by(id=uuid).first()
        if not movie:
            return "", 404
        if current_user.is_admin or current_user == movie.user:
            db.session.delete(movie)
            db.session.commit()
            return {"Success": "Deleted successfully"}, 200
        else:
            return current_app.login_manager.unauthorized()
