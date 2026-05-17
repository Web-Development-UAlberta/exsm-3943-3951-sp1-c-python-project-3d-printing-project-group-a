"""fix order status enum

Revision ID: 7c3aebfed4ba
Revises: 29010949109d
Create Date: 2026-05-17 03:33:27.927359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c3aebfed4ba'
down_revision: Union[str, Sequence[str], None] = '29010949109d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE order_header
        MODIFY COLUMN order_status
        ENUM('Cart', 'Pending', 'Printing', 'Shipped', 'Completed', 'Cancelled')
        NOT NULL
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE order_header
        MODIFY COLUMN order_status
        ENUM('Pending', 'Printing', 'Shipped', 'Completed')
        NOT NULL
    """)