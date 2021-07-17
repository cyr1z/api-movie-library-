""" Movie List Api """
from datetime import datetime

from flask import request, current_app
from flask_login import login_required, current_user
from flask_restx import Resource, fields
from flask_restx.reqparse import RequestParser
from marshmallow import ValidationError
from sqlalchemy import func

from app.models.country import Country
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.resources.api import api
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
        "country_short": fields.String(max_length=2, min_length=2),
    },
)

parser = RequestParser()
parser.add_argument(
    "pageNumber", type=int, required=False, default=1, help="Page number"
)
parser.add_argument("pageSize", type=int, required=False, default=10, help="Page size")
parser.add_argument("searchQuery", type=str, required=False, help="Search query")
parser.add_argument("directorName", type=str, required=False, help="Director name")
parser.add_argument("directorId", type=int, required=False, help="Director ID")
parser.add_argument("genreName", type=str, required=False, help="Genre name")
parser.add_argument("genreId", type=int, required=False, help="Genre ID")
parser.add_argument("yearFrom", type=int, required=False, help="from year")
parser.add_argument("yearTo", type=int, required=False, help="to year")

ORDER_CHOICES = ("date", "dateDesc", "rate", "rateDesc")
parser.add_argument("orderBy", choices=ORDER_CHOICES, help="Bad order by choice")


class MovieListApi(Resource):
    """Movie List Api"""

    movie_schema = MovieSchema()

    @api.expect(parser)
    def get(self):
        """Output a list movies"""
        parser_args = parser.parse_args()

        page = parser_args.get("pageNumber", 1)
        per_page = parser_args.get("pageSize", 10)
        search_query = parser_args.get("searchQuery", "")
        director_name = parser_args.get("directorName", "")
        director_id = parser_args.get("directorId", "")
        genre_name = parser_args.get("genreName", "")
        genre_id = parser_args.get("genreId", "")
        order_by = parser_args.get("orderBy", "")
        year_from = parser_args.get("yearFrom")
        year_to = parser_args.get("yearTo")

        movies = Movie.query

        # By director
        if director_id or director_name:
            director = None
            if director_id:
                director = Director.query.filter(Director.id == director_id).first()
                if not director:
                    api.logger.error(
                        f"[{datetime.now()}], movies, get, {parser_args}, "
                        f'Error: "Wrong Director ID"'
                    )
                    return {"Error": "Wrong Director ID"}, 404
            elif director_name:
                director = Director.query.filter(
                    func.lower(Director.name).contains(director_name.lower())
                ).first()
                if not director:
                    api.logger.error(
                        f"[{datetime.now()}], movies, get, {parser_args}, "
                        f'Error: "Wrong Director name"'
                    )
                    return {"Error": "Wrong Director name"}, 404
            if director:
                movies = movies.filter(Movie.directors.contains(director))

        # By genre
        if genre_id or genre_name:
            genre = None
            if genre_id:
                genre = Genre.query.filter(Genre.id == genre_id).first()
                if not genre:
                    api.logger.error(
                        f"[{datetime.now()}], movies, get, {parser_args}, "
                        f'Error: "Wrong Genre ID"'
                    )
                    return {"Error": "Wrong Genre ID"}, 404
            elif genre_name:
                genre = Genre.query.filter(
                    func.lower(Genre.name).contains(genre_name.lower())
                ).first()
                if not genre:
                    api.logger.error(
                        f"[{datetime.now()}], movies, get, {parser_args}, "
                        f'Error: "Wrong Genre name"'
                    )
                    return {"Error": "Wrong Genre name"}, 404
            if genre:
                movies = movies.filter(Movie.genres.contains(genre))

        # Date from to
        if year_from:
            movies = movies.filter(Movie.released >= f"{year_from}-01-01")
        if year_to:
            movies = movies.filter(Movie.released <= f"{year_to}-12-31")

        # search
        if search_query:
            movies = movies.filter(
                func.lower(Movie.name).contains(search_query.lower())
            )

        # order by
        if order_by and order_by in ORDER_CHOICES:
            if order_by == "date":
                movies = movies.order_by(Movie.released)
            elif order_by == "dateDesc":
                movies = movies.order_by(Movie.released.desc())
            elif order_by == "rate":
                movies = movies.order_by(Movie.rate)
            elif order_by == "rateDesc":
                movies = movies.order_by(Movie.rate.desc())

        # pagination
        movies = movies.paginate(page, per_page, error_out=False)

        api.logger.info(f"[{datetime.now()}], movies, get, {parser_args}, Success")
        return self.movie_schema.dump(movies.items, many=True), 200

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
            api.logger.error(
                f"[{datetime.now()}], movies, post, {data}, Error: {str(error)}, "
                f'"user": {current_user.username}'
            )
            return {"Error": str(error)}, 400

        api.logger.info(
            f"[{datetime.now()}], movies, post, {data}, Success, "
            f'"user": {current_user.username}'
        )
        return self.movie_schema.dump(movie), 201


class MovieApi(Resource):
    """Movie Api"""

    movie_schema = MovieSchema()

    def get(self, uuid=None):
        """Output a single movie"""

        movie = Movie.query.filter_by(id=uuid).first()
        if not movie:
            api.logger.error(
                f'[{datetime.now()}], movies, get, "id": {uuid}, '
                f'Error: "Object was not found'
            )
            return {"Error": "Object was not found"}, 404
        api.logger.info(f'[{datetime.now()}], movies, get, "id": {uuid}, Success')
        return self.movie_schema.dump(movie), 200

    @login_required
    @api.expect(movie_fields, validate=True)
    def put(self, uuid: id):
        """Changing a movie"""

        movie = Movie.query.filter_by(id=uuid).first()
        data = request.json

        if not movie:
            api.logger.error(
                f'[{datetime.now()}], movies, put, "id": {uuid}, '
                f'Error: "Object was not found'
            )
            return {"Error": "Object was not found"}, 404

        if not current_user.is_admin and current_user != movie.user:
            api.logger.error(
                f'[{datetime.now()}], movies, put, "id": {uuid}, '
                f'Error: "NOT AUTHORISED", "user": {current_user.username}'
            )
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
            api.logger.error(
                f"[{datetime.now()}], movies, put, {data}, Error: {str(error)}, "
                f'"user": {current_user.username}'
            )
            return {"Error": str(error)}, 400
        api.logger.info(
            f"[{datetime.now()}], movies, put, {data}, Success, "
            f'"user": {current_user.username}'
        )
        return self.movie_schema.dump(movie), 201

    @staticmethod
    @login_required
    def delete(uuid: int):
        """Delete a movie"""

        movie = Movie.query.filter_by(id=uuid).first()
        if not movie:
            api.logger.info(
                f'[{datetime.now()}], movies, put, "id": {uuid}, '
                f'Error: "Object was not found'
            )
            return "", 404
        if current_user.is_admin or current_user == movie.user:
            movie.delete()
            api.logger.info(
                f'[{datetime.now()}], movies, delete, "id": {uuid},'
                f' Deleted successfully, "user": {current_user.username}'
            )
            return {"Success": "Deleted successfully"}, 200
        else:
            api.logger.error(
                f'[{datetime.now()}], movies, delete, "id": {uuid}, '
                f'Error: "NOT AUTHORISED", "user": {current_user.username}'
            )
            return current_app.login_manager.unauthorized()
