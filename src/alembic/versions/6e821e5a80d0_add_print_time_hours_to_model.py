"""add print_time_hours to model

Revision ID: 6e821e5a80d0
Revises: 893e2b64b2a8
Create Date: 2026-05-09 18:21:49.838100

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '6e821e5a80d0'
down_revision: Union[str, Sequence[str], None] = '893e2b64b2a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('model',
        sa.Column('print_time_hours', sa.DECIMAL(precision=6, scale=2), nullable=True))


def downgrade() -> None:
    op.drop_column('model', 'print_time_hours')