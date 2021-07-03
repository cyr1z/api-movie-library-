""" Top level module """

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
# initialize the database connection
db = SQLAlchemy(app)
# initialize database migration management
migrate = Migrate(app, db)
# API initialize
api = Api(app)


from . import models
# , routes
