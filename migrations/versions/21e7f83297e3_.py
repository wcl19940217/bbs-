"""empty message

Revision ID: 21e7f83297e3
Revises: 749c1009ae98
Create Date: 2018-12-08 00:11:05.294089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21e7f83297e3'
down_revision = '749c1009ae98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('common',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('common')
    # ### end Alembic commands ###
