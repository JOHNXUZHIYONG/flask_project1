"""empty message

Revision ID: b29fb7f076a7
Revises: 3d2771414f50
Create Date: 2023-07-05 14:20:54.140406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b29fb7f076a7'
down_revision = '3d2771414f50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sale_order_id', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('part_number_id', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('prepared_by', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('approved_by', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('approved_by')
        batch_op.drop_column('prepared_by')
        batch_op.drop_column('part_number_id')
        batch_op.drop_column('sale_order_id')

    # ### end Alembic commands ###