""" Movie List Api """

from flask import request, current_app
from flask_login import login_required, current_user
from flask_restx import Resource, fields
from flask_restx.reqparse import RequestParser
from marshmallow import ValidationError

from app.api import api
from app.models import Movie, Country, Genre, Director
from app.schemas.movies import MovieSchema

movie_fields = api.model(
    "Movie",
    {
        "rate": fields.Integer(min=0, max=10),
        "description": fields.String,
        "name": fields.String(required=True),
        "poster_link": fields.String,
        "released": fields.Date,
        "production": fields.String,
        "genres": fields.List(fields.String),
        "directors": fields.List(fields.String),
        "country_name": fields.String,
        "country_short": fields.String,
    },
)

pagination_parser = RequestParser()
pagination_parser.add_argument(
    "pageNumber", type=int, required=False, default=1, help="Page number"
)
pagination_parser.add_argument(
    "pageSize", type=int, required=False, default=10, help="Page size"
)


class MovieListApi(Resource):
    """Movie List Api"""

    movie_schema = MovieSchema()

    @api.expect(pagination_parser)
    def get(self):
        """Output a list movies"""
        p_args = pagination_parser.parse_args()

        page = p_args.get("pageNumber")
        per_page = p_args.get("pageSize")

        movies = Movie.query.paginate(page, per_page, error_out=False).items
        return self.movie_schema.dump(movies, many=True), 200

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
            data["country_name"], data["country_short"]
        )
        for genre in data["genres"]:
            movie.genres.append(Genre.get_or_create(genre))
        for director in data["directors"]:
            movie.directors.append(Director.get_or_create(director))
        try:
            movie.save()
        except ValidationError as error:
            return {"Error": str(error)}, 400

        return self.movie_schema.dump(movie), 201


class MovieApi(Resource):
    """Movie Api"""

    movie_schema = MovieSchema()

    def get(self, uuid=None):
        """Output a single movie"""

        movie = Movie.query.filter_by(id=uuid).first()
        if not movie:
            return {"Error": "Object was not found"}, 404

        return self.movie_schema.dump(movie), 200

    @login_required
    @api.expect(movie_fields, validate=True)
    def put(self, uuid: id):
        """Changing a movie"""

        movie = Movie.query.filter_by(id=uuid).first()
        data = request.json

        if not movie:
            return {"Error": "Object was not found"}, 404

        if not current_user.is_admin and current_user != movie.user:
            return current_app.login_manager.unauthorized()

        movie.rate = data["rate"]
        movie.description = data["description"]
        movie.name = data["name"]
        movie.poster_link = data["poster_link"]
        movie.released = data["released"]
        movie.production = data["production"]
        movie.country = Country.get_or_create(
            data["country_name"], data["country_short"]
        )
        for genre in data["genres"]:
            movie.genres.append(Genre.get_or_create(genre))
        for director in data["directors"]:
            movie.directors.append(Director.get_or_create(director))
        try:
            movie.save()
        except ValidationError as error:
            return {"Error": str(error)}, 400
        return self.movie_schema.dump(movie), 201

    @staticmethod
    @login_required
    def delete(uuid: int):
        """Delete a movie"""

        movie = Movie.query.filter_by(id=uuid).first()
        if not movie:
            return "", 404
        if current_user.is_admin or current_user == movie.user:
            movie.save()
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
