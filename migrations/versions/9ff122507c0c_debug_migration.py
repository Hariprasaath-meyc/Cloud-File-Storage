"""debug migration

Revision ID: 9ff122507c0c
Revises: 4759ad4d2c01
Create Date: 2026-11-21 15:08:05.325881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ff122507c0c'
down_revision: Union[str, Sequence[str], None] = '4759ad4d2c01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
