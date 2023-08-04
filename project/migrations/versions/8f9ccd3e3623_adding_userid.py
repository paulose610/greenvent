"""adding userid

Revision ID: 8f9ccd3e3623
Revises: f67ad833f30a
Create Date: 2023-08-03 18:43:07.952412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f9ccd3e3623'
down_revision = 'f67ad833f30a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_cart_user', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_constraint('fk_cart_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
