""" Top level module """

from flask import Flask
from flask_restx import Api
from flask_login import LoginManager

from .models import Country, User, Movie, Genre, Director, db
from app.config import Config

api = Api()
# login_manager = LoginManager()
# login_manager.login_message_category = "info"


def create_app():
    """ app create """
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize the database connection
    db.init_app(app)
    # API initialize
    api.init_app(
        app,
        title='API Movie Library',
        description='A simple movie library API',
        version='1.0'
    )
    # login_manager.init_app(app)

    return app


app = create_app()

from . import routes


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'user': User,
        'director': Director,
        'genre': Genre,
        'movie': Movie,
        'country': Country
    }
