"""修改了book字段

Revision ID: a3901b9472c9
Revises: d79e303fc234
Create Date: 2022-01-05 03:49:50.288470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3901b9472c9'
down_revision = 'd79e303fc234'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('category', sa.String(length=20), nullable=True))
    op.add_column('book', sa.Column('price', sa.String(length=20), nullable=True))
    op.add_column('book', sa.Column('subtitle', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'subtitle')
    op.drop_column('book', 'price')
    op.drop_column('book', 'category')
    # ### end Alembic commands ###
