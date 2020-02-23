"""add time fetched

Revision ID: 2ac12eb08e6f
Revises: be3bcd7f31e6
Create Date: 2020-02-23 18:28:56.898431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ac12eb08e6f'
down_revision = 'be3bcd7f31e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timefetched',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timefetched')
    # ### end Alembic commands ###
