""" Api module """
import logging

from flask_restx import Api

from app.config import LOG_PATH, LOG_LEVEL

api = Api()

# configure logger
NAME_TO_LEVEL = {
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def name_to_log_level(level_name):
    return NAME_TO_LEVEL[level_name]


logging.basicConfig(level=name_to_log_level(LOG_LEVEL))
file_handler = logging.FileHandler(LOG_PATH)
api.logger.addHandler(file_handler)
