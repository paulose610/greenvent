"""unique user

Revision ID: e91d3159b1a4
Revises: 8d24f38d84ed
Create Date: 2023-08-12 15:32:10.546506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e91d3159b1a4'
down_revision = '8d24f38d84ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('uname',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('uname',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)

    # ### end Alembic commands ###
