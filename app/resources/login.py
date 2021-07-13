from flask import request, jsonify
from flask_login import login_user, logout_user
from flask_restx import Namespace, Resource, fields

from app.api import api
from app.models import User

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
        result = jsonify({'result': 200, 'data': {'message': 'login success'}})

        if user and user.verify_password(post_data['password']):
            login_user(user)
        else:
            result = jsonify({"status": 401, "reason": "Incorrect username or password"})

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
        logout_user()
        return jsonify({'result': 200, 'data': {'message': 'logout success'}})
