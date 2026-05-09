"""merge heads

Revision ID: 130f7356d5c1
Revises: 0cd4f77e0e19, 1234567890
Create Date: 2026-05-07 23:42:50.775017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '130f7356d5c1'
down_revision: Union[str, Sequence[str], None] = ('0cd4f77e0e19', '1234567890')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
