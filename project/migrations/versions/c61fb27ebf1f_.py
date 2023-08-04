"""empty message

Revision ID: c61fb27ebf1f
Revises: d594838bcd76
Create Date: 2023-08-03 23:23:08.148550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c61fb27ebf1f'
down_revision = 'd594838bcd76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.create_foreign_key('fkpid', 'prod', ['Pid'], ['id'])
        batch_op.drop_column('no')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('no', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint('fkpid', type_='foreignkey')

    # ### end Alembic commands ###
