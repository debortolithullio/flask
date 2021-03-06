"""create all database

Revision ID: 70daa96fb4ff
Revises: 
Create Date: 2019-11-20 12:33:27.664745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70daa96fb4ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('investment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('category', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investment_category'), 'investment', ['category'], unique=False)
    op.create_index(op.f('ix_investment_title'), 'investment', ['title'], unique=True)
    op.create_table('investment_goal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investment_goal_year'), 'investment_goal', ['year'], unique=True)
    op.create_table('item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('mtype', sa.String(length=30), nullable=True),
    sa.Column('category', sa.String(length=140), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_category'), 'item', ['category'], unique=False)
    op.create_index(op.f('ix_item_date'), 'item', ['date'], unique=False)
    op.create_table('position',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('investment', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('net_amount', sa.Float(), nullable=True),
    sa.Column('gross_amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['investment'], ['investment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_position_date'), 'position', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_position_date'), table_name='position')
    op.drop_table('position')
    op.drop_index(op.f('ix_item_date'), table_name='item')
    op.drop_index(op.f('ix_item_category'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_investment_goal_year'), table_name='investment_goal')
    op.drop_table('investment_goal')
    op.drop_index(op.f('ix_investment_title'), table_name='investment')
    op.drop_index(op.f('ix_investment_category'), table_name='investment')
    op.drop_table('investment')
    # ### end Alembic commands ###
