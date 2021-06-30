""" Top level module """

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api
from app.config import Config

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=Config.DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=Config.SQLALCHEMY_TRACK_MODIFICATIONS,
)

# initialize the database connection
db = SQLAlchemy(app)

# API initialize
api = Api(app)

# initialize database migration management
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello World!'


#
# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}


# from app import routes, models

if __name__ == '__main__':
    app.run()
