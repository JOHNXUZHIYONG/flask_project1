"""empty message

Revision ID: 3a179390b88e
Revises: 4ae3c95cc411
Create Date: 2023-07-03 14:25:17.526584

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3a179390b88e'
down_revision = '4ae3c95cc411'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status1', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('sentencing_time1', sa.String(), nullable=False))
        batch_op.drop_column('quantity2')
        batch_op.drop_column('price1')
        batch_op.drop_column('price2')
        batch_op.drop_column('item3')
        batch_op.drop_column('quantity1')
        batch_op.drop_column('total_price')
        batch_op.drop_column('item2')
        batch_op.drop_column('price3')
        batch_op.drop_column('quantity3')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity3', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('price3', mysql.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('item2', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('total_price', mysql.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('quantity1', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('item3', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('price2', mysql.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('price1', mysql.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('quantity2', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('sentencing_time1')
        batch_op.drop_column('status1')

    # ### end Alembic commands ###
