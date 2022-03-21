"""add_collected_at_field_to_noaa_stations

Revision ID: de40b6695d52
Revises: 88f5448ba9d8
Create Date: 2022-03-17 15:47:28.688136

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'de40b6695d52'
down_revision = '88f5448ba9d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('noaastationss', sa.Column('collected_at', sa.DateTime(), nullable=True))
    op.alter_column('noaastationss', 'geometry',
               existing_type=ga.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('noaastationss', 'geometry',
               existing_type=ga.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'),
               nullable=True)
    op.drop_column('noaastationss', 'collected_at')
    # ### end Alembic commands ###
