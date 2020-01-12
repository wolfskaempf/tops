"""add archival status

Revision ID: 18b067cccf4f
Revises: 3f6741e8dc8d
Create Date: 2020-01-12 00:32:45.587560

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '18b067cccf4f'
down_revision = '3f6741e8dc8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('top', sa.Column('archiviert', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('top', 'archiviert')
    # ### end Alembic commands ###
