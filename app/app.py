""" Top level module """

from flask import Flask

from .api import api
from .login import login_manager
from .models import Country, User, Movie, Genre, Director, db
from .config import Config


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

from . import routes


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "user": User,
        "director": Director,
        "genre": Genre,
        "movie": Movie,
        "country": Country,
    }
