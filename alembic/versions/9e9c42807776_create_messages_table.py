"""Create messages table

Revision ID: 9e9c42807776
Revises: 
Create Date: 2025-12-18 04:55:29.146350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e9c42807776'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tier', sa.String(), nullable=True),
        sa.Column('query', sa.String(), nullable=True),
        sa.Column('response', sa.String(), nullable=True),
        sa.Column('timestamp', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('messages')
