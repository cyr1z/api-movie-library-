""" Top level module """

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# import click
# from seeder import ResolvingSeeder

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
# initialize the database connection
db = SQLAlchemy(app)
# initialize database migration management
migrate = Migrate(app, db)
# API initialize
api = Api(
    app,
    title='API Movie Library',
    description='A simple movie library API',
    version='1.0'
)

login = LoginManager(app)

from .models import Country, User, Movie, Genre, Director
from . import routes

login_manager = LoginManager(app)
login_manager.login_message_category = "info"

from .models import Country, User, Movie, Genre, Director
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
