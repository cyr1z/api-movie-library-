""" Top level module """

from flask import Flask

from .config import Config
from .login import login_manager
from .models import db
from .models.country import Country
from .models.director import Director
from .models.genre import Genre
from .models.movie import Movie
from .models.user import User
from .resources.api import api
from . import routes


def create_app():
    """app create"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize the database connection
    db.init_app(app)
    # API initialize
    api.init_app(
        app,
        title="API Movie Library",
        description="A simple movie library API",
        version="1.0",
    )
    login_manager.init_app(app)

    return app


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """set shell context"""
    return {
        "db": db,
        "user": User,
        "director": Director,
        "genre": Genre,
        "movie": Movie,
        "country": Country,
    }
