""" login manager module """

from flask_login import LoginManager

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
