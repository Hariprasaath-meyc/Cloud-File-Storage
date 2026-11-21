"""extend_file_status_enum

Revision ID: 9f84af31b8c2
Revises: 9b46a2857558
Create Date: 2026-11-21 11:52:28.735272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f84af31b8c2'
down_revision: Union[str, Sequence[str], None] = '9b46a2857558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
        op.execute(
        "ALTER TYPE file_status ADD VALUE IF NOT EXISTS 'PROCESSING'"
    )

        op.execute(
        "ALTER TYPE file_status ADD VALUE IF NOT EXISTS 'EXPIRED'"
    )



def downgrade() -> None:
    """Downgrade schema."""
    pass
