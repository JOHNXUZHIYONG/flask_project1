"""empty message

Revision ID: 1a94df192ee6
Revises: b29fb7f076a7
Create Date: 2023-07-05 14:41:48.216939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a94df192ee6'
down_revision = 'b29fb7f076a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('part_id', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('part_id')

    # ### end Alembic commands ###
