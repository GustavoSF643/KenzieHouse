"""Merging migrations heads

Revision ID: 697c91194c86
Revises: 8089134f8e3f, 4916c6cfde7f
Create Date: 2021-10-11 17:39:03.713279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '697c91194c86'
down_revision = ('8089134f8e3f', '4916c6cfde7f')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
