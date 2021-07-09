"""add short for countries

Revision ID: b89fd6c8f637
Revises: 32d78df47db9
Create Date: 2021-07-08 20:17:04.568662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b89fd6c8f637'
down_revision = '32d78df47db9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Country', sa.Column('short', sa.String(length=4), nullable=True))
    op.create_index(op.f('ix_Country_short'), 'Country', ['short'], unique=True)
    op.drop_index('ix_Movie_email', table_name='Movie')
    op.drop_column('Movie', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Movie', sa.Column('email', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.create_index('ix_Movie_email', 'Movie', ['email'], unique=False)
    op.drop_index(op.f('ix_Country_short'), table_name='Country')
    op.drop_column('Country', 'short')
    # ### end Alembic commands ###
