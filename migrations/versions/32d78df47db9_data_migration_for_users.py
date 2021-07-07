"""data migration for users

Revision ID: 32d78df47db9
Revises: 9255dbcb8a36
Create Date: 2021-07-07 15:22:52.877584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from faker import Faker
from werkzeug.security import generate_password_hash

from app.models import User

revision = '32d78df47db9'
down_revision = '9255dbcb8a36'
branch_labels = None
depends_on = None


class FakeUser(User):
    def __init__(self, fake):
        self.email = fake.ascii_email()
        self.username = fake.first_name().lower() + '_' + fake.last_name().lower()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.is_admin = False


user_table = User.__table__


def fake_users(num):
    fake = Faker('en_US')
    users = [{
        'email': 'admin@admin.com',
        'first_name': 'admin',
        'last_name': 'admin',
        'username': 'admin',
        'password_hash': generate_password_hash('admin'),
        'is_admin': True
    }]
    for _ in range(num):
        user = FakeUser(fake)
        user.password = user.username

        users.append(
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'password_hash': user.password_hash,
                'is_admin': user.is_admin
            }
        )

    return users


def upgrade():
    new_users = fake_users(250)
    op.bulk_insert(user_table, new_users)


def downgrade():
    user_table.delete()
