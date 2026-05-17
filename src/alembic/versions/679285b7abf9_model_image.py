"""model_image

Revision ID: 679285b7abf9
Revises: 7c3aebfed4ba
Create Date: 2026-05-17 06:11:57.004038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '679285b7abf9'
down_revision: Union[str, Sequence[str], None] = '7c3aebfed4ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'model',
        sa.Column('model_image', sa.String(length=255), nullable=True)
    )

def downgrade():
    op.drop_column('model', 'model_image')