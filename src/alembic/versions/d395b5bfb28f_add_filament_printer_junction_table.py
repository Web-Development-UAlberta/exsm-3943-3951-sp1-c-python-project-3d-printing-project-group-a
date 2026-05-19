"""add filament_printer junction table

Revision ID: d395b5bfb28f
Revises: 2499929c07a6
Create Date: 2026-05-19 17:57:33.526369
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd395b5bfb28f'
down_revision: Union[str, Sequence[str], None] = '2499929c07a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create the new many-to-many junction table
    op.create_table(
        'filament_printer',
        sa.Column('printer_id', sa.Integer(), nullable=False),
        sa.Column('filament_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['printer_id'],
            ['printer.printer_id']
        ),
        sa.ForeignKeyConstraint(
            ['filament_id'],
            ['filament.filament_id']
        ),
        sa.PrimaryKeyConstraint(
            'printer_id',
            'filament_id'
        )
    )

    # Find and drop the existing foreign key on printer.filament_id
    conn = op.get_bind()

    result = conn.execute(sa.text("""
        SELECT CONSTRAINT_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'printer'
          AND COLUMN_NAME = 'filament_id'
          AND REFERENCED_TABLE_NAME = 'filament'
    """))

    row = result.fetchone()
    if row:
        fk_name = row[0]
        op.drop_constraint(fk_name, 'printer', type_='foreignkey')

    # Now remove the old column
    op.drop_column('printer', 'filament_id')



def downgrade() -> None:
    """Downgrade schema."""

    # Restore the old filament_id column
    op.add_column(
        'printer',
        sa.Column(
            'filament_id',
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=True
        )
    )

    op.create_foreign_key(
        None,
        'printer',
        'filament',
        ['filament_id'],
        ['filament_id']
    )

    # Drop the junction table
    op.drop_table('filament_printer')