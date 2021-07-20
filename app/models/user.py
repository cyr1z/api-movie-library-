""" User model """

from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

from . import db


class User(UserMixin, db.Model):
    """User model for storing user related data"""

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(50), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password: str):
        """password setter"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        """verify password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return f"{self.email}, {self.username} {self.first_name} {self.last_name}"

    @classmethod
    def find_by_username(cls, username: str):
        """find user by username"""
        return User.query.filter(User.username == username).first()

    @classmethod
    def get_random(cls):
        """get random user"""
        return User.query.order_by(func.random()).first()

    @classmethod
    def find_by_email(cls, email: str):
        """find user by email"""
        return User.query.filter(User.email == email).first()

    def save(self):
        """save"""
        db.session.add(self)
        db.session.commit()
        return self
