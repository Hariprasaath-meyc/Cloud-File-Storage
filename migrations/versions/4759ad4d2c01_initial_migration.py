"""initial migration

Revision ID: 4759ad4d2c01
Revises: c6236f1ffe62
Create Date: 2026-11-21 15:03:55.272644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4759ad4d2c01'
down_revision: Union[str, Sequence[str], None] = 'c6236f1ffe62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
