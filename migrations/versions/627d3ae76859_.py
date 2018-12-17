"""empty message

Revision ID: 627d3ae76859
Revises: 6a8301c9a797
Create Date: 2018-12-06 16:31:54.328607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '627d3ae76859'
down_revision = '6a8301c9a797'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('link_url', sa.String(length=255), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banner')
    # ### end Alembic commands ###
