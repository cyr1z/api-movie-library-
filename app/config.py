""" Config from actual .env file """

from os import getenv

POSTGRES_DB = getenv("POSTGRES_DB")
APP_NAME = getenv("APP_NAME")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")


class Config:
    """config"""

    DEBUG = not bool(getenv("PROD"))
    SECRET_KEY = getenv("SECRET_KEY")
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@db-{APP_NAME}:5432/{POSTGRES_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
