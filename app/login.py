import base64

from flask import request, jsonify
from flask_login import LoginManager, login_user

from app.models import User

login_manager = LoginManager()
login_manager.login_message_category = "info"
login_manager.session_protection = "basic"


@login_manager.user_loader
def load_user(uuid):
    """
    User loader
    :param uuid: user id
    :return: error message or json with user data
    """
    return User.query.get(int(uuid))


def login():
    """
    user login
    :return: error message or successful message
    """
    user_json = request.get_json()
    user = User.find_by_username(user_json['username'])
    result = jsonify({'result': 200, 'data': {'message': 'login success'}})

    if user and user.verify_password(user_json['user_password']):
        login_user(user)
    else:
        result = jsonify({"status": 401, "reason": "Incorrect username or password"})

    return result
