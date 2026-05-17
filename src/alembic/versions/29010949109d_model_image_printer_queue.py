"""model_image, printer_queue

Revision ID: 29010949109d
Revises: fba46752398b
Create Date: 2026-05-17 03:29:42.001237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '29010949109d'
down_revision: Union[str, Sequence[str], None] = 'fba46752398b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'printer',
        sa.Column('printer_queue', sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('printer', 'printer_queue')