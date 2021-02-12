"""empty message

Revision ID: f0dc86199964
Revises: 2f605fc0cb50
Create Date: 2021-02-12 17:40:24.467618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0dc86199964'
down_revision = '2f605fc0cb50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('likepost', 'comments')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likepost', sa.Column('comments', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###
