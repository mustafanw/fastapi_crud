"""Add new column

Revision ID: 6320e1bb0686
Revises: 46ddfb6e4ada
Create Date: 2024-02-18 15:50:10.062235

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6320e1bb0686'
down_revision = '46ddfb6e4ada'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('players_user_id_fkey', 'players', type_='foreignkey')
    op.drop_column('players', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('players_user_id_fkey', 'players', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
