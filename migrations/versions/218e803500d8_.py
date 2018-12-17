"""empty message

Revision ID: 218e803500d8
Revises: 1e4ff237c3b7
Create Date: 2018-12-09 17:01:47.010217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '218e803500d8'
down_revision = '1e4ff237c3b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('comment_nums', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'comment_nums')
    # ### end Alembic commands ###