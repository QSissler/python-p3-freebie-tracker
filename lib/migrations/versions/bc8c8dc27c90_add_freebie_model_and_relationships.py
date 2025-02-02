"""Add Freebie model and relationships

Revision ID: bc8c8dc27c90
Revises: ee905476242e
Create Date: 2023-02-21 17:29:50.582018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc8c8dc27c90'
down_revision = 'ee905476242e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('freebies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('dev_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['dev_id'], ['devs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('freebies')
    # ### end Alembic commands ###
