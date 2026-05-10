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
    op.create_table('model_tag',
        sa.Column('model_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['model_id'], ['model.model_id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.tag_id']),
        sa.PrimaryKeyConstraint('model_id', 'tag_id')
    )
    op.alter_column('filament', 'filament_price',
        type_=sa.DECIMAL(precision=10, scale=2), existing_nullable=False)
    op.alter_column('order_detail', 'unit_price',
        type_=sa.DECIMAL(precision=10, scale=2), existing_nullable=True)
    op.alter_column('order_header', 'shipping_price',
        type_=sa.DECIMAL(precision=10, scale=2), existing_nullable=False)
    op.alter_column('order_header', 'extra_fee',
        type_=sa.DECIMAL(precision=10, scale=2), existing_nullable=True)
    op.alter_column('order_header', 'total_price',
        type_=sa.DECIMAL(precision=10, scale=2), existing_nullable=False)
    with op.batch_alter_table('model') as batch_op:
        batch_op.drop_column('tag_id')


def downgrade() -> None:
    with op.batch_alter_table('model') as batch_op:
        batch_op.add_column(sa.Column('tag_id', sa.Integer(), nullable=True))
    op.alter_column('order_header', 'total_price',
        type_=sa.Float(), existing_nullable=False)
    op.alter_column('order_header', 'extra_fee',
        type_=sa.Float(), existing_nullable=True)
    op.alter_column('order_header', 'shipping_price',
        type_=sa.Float(), existing_nullable=False)
    op.alter_column('order_detail', 'unit_price',
        type_=sa.Float(), existing_nullable=True)
    op.alter_column('filament', 'filament_price',
        type_=sa.Float(), existing_nullable=False)
    op.drop_table('model_tag')