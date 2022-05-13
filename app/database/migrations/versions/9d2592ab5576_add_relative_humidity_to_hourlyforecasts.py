"""add_relative_humidity_to_hourlyforecasts

Revision ID: 9d2592ab5576
Revises: 9375d66131ad
Create Date: 2022-03-22 11:40:32.061984

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga


# revision identifiers, used by Alembic.
revision = '9d2592ab5576'
down_revision = '9375d66131ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hourlyforecasts', sa.Column('relative_humidity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hourlyforecasts', 'relative_humidity')
    # ### end Alembic commands ###