"""usitem table

Revision ID: 5cbdbbfd3390
Revises: 
Create Date: 2019-11-04 08:43:50.016676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cbdbbfd3390'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('category', sa.String(length=140), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_category'), 'item', ['category'], unique=False)
    op.create_index(op.f('ix_item_date'), 'item', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_date'), table_name='item')
    op.drop_index(op.f('ix_item_category'), table_name='item')
    op.drop_table('item')
    # ### end Alembic commands ###
