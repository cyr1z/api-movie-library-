from flask_restx import Resource
from sqlalchemy import func

from app.models import Movie, db


class AggregationsApi(Resource):
    def get(self):
        movies_count = db.session.query(func.count(Movie.id)).scalar()
        max_rating = db.session.query(func.max(Movie.rating)).scalar()
        min_rating = db.session.query(func.min(Movie.rating)).scalar()
        avg_rating = db.session.query(func.avg(Movie.rating)).scalar()
        sum_rating = db.session.query(func.sum(Movie.rating)).scalar()
        return {
            "count": movies_count,
            "max": max_rating,
            "min": min_rating,
            "avg": avg_rating,
            "sum": sum_rating,
        }
