""" Aggregations """

from flask_restx import Resource
from sqlalchemy import func

from app.models import db
from app.models.movie import Movie


class AggregationsApi(Resource):
    """ aggregations """
    def get(self):
        movies_count = db.session.query(func.count(Movie.id)).scalar()
        max_rating = db.session.query(func.max(Movie.rate)).scalar()
        min_rating = db.session.query(func.min(Movie.rate)).scalar()
        avg_rating = db.session.query(func.avg(Movie.rate)).scalar()
        min_year = db.session.query(func.min(Movie.released)).scalar().year
        max_year = db.session.query(func.max(Movie.released)).scalar().year
        return {
            "count": movies_count,
            "max_rate": max_rating,
            "min_rate": min_rating,
            "avg_rate": avg_rating,
            "min_year": min_year,
            "max_year": max_year,
        }
