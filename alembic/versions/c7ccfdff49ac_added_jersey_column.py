"""added jersey column

Revision ID: c7ccfdff49ac
Revises: bd30d743e753
Create Date: 2024-02-18 17:02:13.906061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ccfdff49ac'
down_revision = 'bd30d743e753'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('jersey_name', sa.String(), nullable=False))
    op.add_column('players', sa.Column('jersey_number', sa.Numeric(), nullable=False))
    op.create_unique_constraint(None, 'players', ['jersey_name'])
    op.create_unique_constraint(None, 'players', ['jersey_number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'players', type_='unique')
    op.drop_constraint(None, 'players', type_='unique')
    op.drop_column('players', 'jersey_number')
    op.drop_column('players', 'jersey_name')
    # ### end Alembic commands ###