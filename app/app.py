""" Top level module """

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from app.config import Config

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=Config.DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=Config.SQLALCHEMY_TRACK_MODIFICATIONS,
)

engine = create_engine(Config.DATABASE_URI, echo=True)
# initialize the database connection
db = SQLAlchemy(app)

# API initialize
api = Api(app)

# initialize database migration management
migrate = Migrate(app, db)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


#
# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}


