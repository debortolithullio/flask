"""poupdate position table

Revision ID: cf60b7f4dbac
Revises: bfa7c103a5c4
Create Date: 2019-11-11 13:36:29.022324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf60b7f4dbac'
down_revision = 'bfa7c103a5c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('position', sa.Column('gross_amount', sa.Float(), nullable=True))
    op.add_column('position', sa.Column('net_amount', sa.Float(), nullable=True))
    op.drop_column('position', 'position')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('position', sa.Column('position', sa.FLOAT(), nullable=True))
    op.drop_column('position', 'net_amount')
    op.drop_column('position', 'gross_amount')
    # ### end Alembic commands ###
