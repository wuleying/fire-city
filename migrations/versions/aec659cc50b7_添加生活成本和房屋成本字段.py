"""添加生活成本和房屋成本字段

Revision ID: aec659cc50b7
Revises: 1f2d9671f786
Create Date: 2025-01-01 20:52:35.143742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aec659cc50b7'
down_revision = '1f2d9671f786'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cost_of_living', sa.Numeric(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('housing_cost', sa.Numeric(precision=10, scale=2), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cities', schema=None) as batch_op:
        batch_op.drop_column('housing_cost')
        batch_op.drop_column('cost_of_living')

    # ### end Alembic commands ###
