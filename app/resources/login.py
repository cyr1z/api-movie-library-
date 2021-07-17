"""
Login Api

"""
from datetime import datetime

from flask import request, jsonify
from flask_login import login_user, logout_user, current_user
from flask_restx import Namespace, Resource, fields

from app.models.user import User
from app.resources.api import api

auth_namespace = Namespace("auth")

auth = api.model(
    "Login",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


class Login(Resource):
    """
    user login
    """

    @auth_namespace.expect(auth, validate=True)
    def post(self):
        """
        user login
        :return: error message or successful message
        """
        post_data = request.get_json()
        user = User.find_by_username(post_data.get("username"))
        result = jsonify({"result": 200, "data": {"message": "login success"}})

        if user and user.verify_password(post_data["password"]):
            login_user(user)
            api.logger.info(
                f'[{datetime.now()}], login, post, "user": {user.username}, ' f"Success"
            )
        else:
            result = jsonify(
                {"status": 401, "reason": "Incorrect username or password"}
            )
            api.logger.info(
                f'[{datetime.now()}], login, post, "user": {post_data.get("username")}, '
                f'Error: "Incorrect username or password"'
            )
        return result


class Logout(Resource):
    """
    user logout
    """

    def post(self):
        """
        user logout
        :return: error message or successful message
        """
        try:
            username = current_user.username
            logout_user()
            api.logger.info(
                f'[{datetime.now()}], logout, post, Success, "user": {username}'
            )
            return jsonify({"result": 200, "data": {"message": "logout success"}})

        except AttributeError as error:
            api.logger.info(f"[{datetime.now()}], logout, post, Error: {str(error)}")
            jsonify({"result": 401, "data": {"Error": "user not logged"}})
