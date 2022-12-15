"""empty message

Revision ID: de8ec32b4dff
Revises: 5cf9d3764315
Create Date: 2022-11-18 15:23:56.240025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de8ec32b4dff'
down_revision = '5cf9d3764315'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tarea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=False),
    sa.Column('label', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tarea')
    # ### end Alembic commands ###
