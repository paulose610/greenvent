"""adding cat,prod and user

Revision ID: 2926ed772ff4
Revises: 
Create Date: 2023-07-28 00:49:16.706341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2926ed772ff4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cname', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cname')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uname', sa.String(length=30), nullable=False),
    sa.Column('pswdhash', sa.String(length=60), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uname')
    )
    op.create_table('prod',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('catid', sa.Integer(), nullable=False),
    sa.Column('pname', sa.String(length=30), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(length=15), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('sold', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['catid'], ['cat.id'], name='fkpc'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pname')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prod')
    op.drop_table('user')
    op.drop_table('cat')
    # ### end Alembic commands ###
