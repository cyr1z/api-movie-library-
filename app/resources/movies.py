""" Movie List Api """

from flask import request, current_app
from flask_login import login_required, current_user
from flask_restx import Resource, fields, Namespace
from marshmallow import ValidationError

from app.api import api
from app.models import Movie, db, Country, Genre, Director
from app.schemas.movies import MovieSchema

movie_fields = api.model(
    "Movie",
    {
        "rate": fields.Integer(min=0, max=10),
        "description": fields.String,
        "name": fields.String(required=True),
        "poster_link": fields.Url,
        "released": fields.Date,
        "production": fields.String,
        "genres": fields.String,
        "directors": fields.String,
        "country": fields.String,
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

    # @login_required
    # @api.expect(movie_fields, validate=True)
    # def post(self):
    #     """Adding a movie"""
    #
    #     try:
    #         movie = self.movie_schema.load(request.json, session=db.session)
    #     except ValidationError as error:
    #         return {"Error": str(error)}, 400
    #
    #     db.session.add(movie)
    #     db.session.commit()
    #     return self.movie_schema.dump(movie), 201

    @login_required
    @api.expect(movie_fields, validate=True)
    def post(self):
        """Adding a movie"""

        data = request.json
        movie = Movie()

        movie.user = current_user
        movie.rate = data["rate"]
        movie.description = data["description"]
        movie.name = data["name"]
        movie.poster_link = data["poster_link"]
        movie.released = data["released"]
        movie.production = data["production"]
        movie.country = Country.get_or_create(
            data["country"]["name"], data["country"]["short"]
        )
        for genre in data["genres"]:
            movie.genres.append(Genre.get_or_create(genre))
        for director in data["directors"]:
            movie.directors.append(Director.get_or_create(director))

        return movie.save()


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


class MovieSearchApi(Resource):
    """Search Movie Api"""

    movie_schema = MovieSchema()

    def get(self, target):
        """Output matched movies"""

        movies = Movie.search(target)
        return self.movie_schema.dump(movies, many=True), 200
