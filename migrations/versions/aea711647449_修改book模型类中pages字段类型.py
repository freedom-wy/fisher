"""修改book模型类中pages字段类型

Revision ID: aea711647449
Revises: dc949c32e0ba
Create Date: 2022-01-11 15:14:11.768904

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aea711647449'
down_revision = 'dc949c32e0ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'pages',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=10),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'pages',
               existing_type=sa.String(length=10),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=True)
    # ### end Alembic commands ###
