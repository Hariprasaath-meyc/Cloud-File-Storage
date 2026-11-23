from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# Alembic revision identifiers
revision = "06fdd5024e35"
down_revision = "9ff122507c0c"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # 1. Add nullable column
    op.add_column(
        "files",
        sa.Column(
            "idempotency_key",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )

    # 2. Populate existing records
    op.execute(
        """
        UPDATE files
        SET idempotency_key = gen_random_uuid()
        WHERE idempotency_key IS NULL
        """
    )

    # 3. Make it NOT NULL
    op.alter_column(
        "files",
        "idempotency_key",
        nullable=False,
    )

    # 4. Add unique constraint
    op.create_unique_constraint(
        "uq_files_idempotency_key",
        "files",
        ["idempotency_key"],
    )


def downgrade() -> None:

    op.drop_constraint(
        "uq_files_idempotency_key",
        "files",
        type_="unique",
    )

    op.drop_column("files", "idempotency_key")