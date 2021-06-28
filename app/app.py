from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=Config.DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=Config.SQLALCHEMY_TRACK_MODIFICATIONS,
)

# initialize the database connection
db = SQLAlchemy(app)

# initialize database migration management
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
