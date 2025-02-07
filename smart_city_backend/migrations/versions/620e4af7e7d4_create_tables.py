"""Create tables

Revision ID: 620e4af7e7d4
Revises: 
Create Date: 2025-02-07 17:25:55.260463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '620e4af7e7d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metering',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('water_usage', sa.Float(), nullable=False),
    sa.Column('energy_usage', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pollution',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('air_quality_index', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('traffic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('congestion_level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('waste',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('bin_fill_level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('waste')
    op.drop_table('traffic')
    op.drop_table('pollution')
    op.drop_table('metering')
    # ### end Alembic commands ###
