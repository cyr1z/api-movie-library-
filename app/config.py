""" Config from actual .env file """

from os import getenv


class Config:
    """ config """
    DEBUG = not bool(getenv('PROD'))
    HOST = getenv('HOST')
    SECRET_KEY = getenv('SECRET_KEY')
    POSTGRES_DB = getenv('POSTGRES_DB')
    APP_NAME = getenv('APP_NAME')
    POSTGRES_USER = getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
    DB_PORT = getenv('DB_PORT')
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}' \
                   f'@db-{APP_NAME}:{DB_PORT}/{POSTGRES_DB}'
