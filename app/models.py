from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    """Simple database model to track event attendees."""

    # u = User(email="test@examplesite.com", phone_number="1111111111")
    # u.set_password('P@ssw0rd')
    # db.session.add(u)
    # db.session.commit()

    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    phone_number = db.Column(db.String(16), index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email=None):
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.id

    def __str__(self):
        return f"{self.email}, {self.first_name} {self.last_name}"
