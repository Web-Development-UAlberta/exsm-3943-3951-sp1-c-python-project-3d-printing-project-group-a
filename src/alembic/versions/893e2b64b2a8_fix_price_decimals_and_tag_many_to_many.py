"""fix price decimals and tag many-to-many

Revision ID: 893e2b64b2a8
Revises: 332b152d0924
Create Date: 2026-05-08 23:50:06.089685

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '893e2b64b2a8'
down_revision: Union[str, Sequence[str], None] = '332b152d0924'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # create model_tag junction table
    op.create_table('model_tag',
        sa.Column('model_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['model_id'], ['Model.model_id']),
        sa.ForeignKeyConstraint(['tag_id'], ['Tag.tag_id']),
        sa.PrimaryKeyConstraint('model_id', 'tag_id')
    )

    # fix price fields to DECIMAL
    op.alter_column('Filament', 'filament_price',
        type_=sa.DECIMAL(precision=10, scale=2),
        existing_nullable=False
    )
    op.alter_column('Order_Detail', 'unit_price',
        type_=sa.DECIMAL(precision=10, scale=2),
        existing_nullable=True
    )
    op.alter_column('Order_Header', 'shipping_price',
        type_=sa.DECIMAL(precision=10, scale=2),
        existing_nullable=False
    )
    op.alter_column('Order_Header', 'extra_fee',
        type_=sa.DECIMAL(precision=10, scale=2),
        existing_nullable=True
    )
    op.alter_column('Order_Header', 'total_price',
        type_=sa.DECIMAL(precision=10, scale=2),
        existing_nullable=False
    )

    # remove old direct tag FK from model
    op.drop_column('Model', 'tag_id')


def downgrade() -> None:
    op.add_column('Model',
        sa.Column('tag_id', sa.Integer(), nullable=True)
    )
    op.alter_column('Order_Header', 'total_price',
        type_=sa.Float(),
        existing_nullable=False
    )
    op.alter_column('Order_Header', 'extra_fee',
        type_=sa.Float(),
        existing_nullable=True
    )
    op.alter_column('Order_Header', 'shipping_price',
        type_=sa.Float(),
        existing_nullable=False
    )
    op.alter_column('Order_Detail', 'unit_price',
        type_=sa.Float(),
        existing_nullable=True
    )
    op.alter_column('Filament', 'filament_price',
        type_=sa.Float(),
        existing_nullable=False
    )
    op.drop_table('model_tag')