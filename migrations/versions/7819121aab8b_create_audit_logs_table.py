
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "7819121aab8b"
down_revision = "06fdd5024e35"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "event_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "actor_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),

        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(50), nullable=False),
        sa.Column("resource_id", sa.String(255), nullable=True),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("source", sa.String(50), nullable=False),

        sa.Column(
            "event_time",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column("details", postgresql.JSONB(), nullable=True),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "event_id",
            name="uq_audit_logs_event_id",
        ),
    )

    op.create_index(
        "ix_audit_logs_actor_id",
        "audit_logs",
        ["actor_id"],
    )

    op.create_index(
        "ix_audit_logs_action",
        "audit_logs",
        ["action"],
    )

    op.create_index(
        "ix_audit_logs_event_time",
        "audit_logs",
        ["event_time"],
    )

    op.create_index(
        "ix_audit_logs_resource",
        "audit_logs",
        ["resource_type", "resource_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_audit_logs_resource", table_name="audit_logs")
    op.drop_index("ix_audit_logs_event_time", table_name="audit_logs")
    op.drop_index("ix_audit_logs_action", table_name="audit_logs")
    op.drop_index("ix_audit_logs_actor_id", table_name="audit_logs")

    op.drop_table("audit_logs")
