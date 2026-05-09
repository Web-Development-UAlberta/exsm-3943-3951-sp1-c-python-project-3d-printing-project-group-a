"""add password to users

Revision ID: 332b152d0924
Revises: 130f7356d5c1
Create Date: 2026-05-07 23:43:07.281207

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '332b152d0924'
down_revision: Union[str, Sequence[str], None] = '130f7356d5c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',
        sa.Column('password', sa.String(255), nullable=False, server_default='')
    )


def downgrade() -> None:
    op.drop_column('users', 'password')