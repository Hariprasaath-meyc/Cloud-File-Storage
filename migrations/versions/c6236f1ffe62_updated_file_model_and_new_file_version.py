
"""Create file versions and update files

Revision ID: create_file_versions
Revises: your_previous_revision
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c6236f1ffe62"
down_revision: str = "9f84af31b8c2"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Add upload expiration to files table.
    op.add_column(
        "files",
        sa.Column(
            "upload_expires_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # Backfill existing records before making the column mandatory.
    op.execute("""
        UPDATE files
        SET upload_expires_at = created_at + INTERVAL '30 minutes'
        WHERE upload_expires_at IS NULL
    """)

    op.alter_column(
        "files",
        "upload_expires_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )

    # Create index for file status.
    op.create_index(
        "ix_files_status",
        "files",
        ["status"],
        unique=False,
    )

    # Create file_versions table.
    op.create_table(
        "file_versions",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "file_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "bucket_name",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "object_key",
            sa.String(length=1024),
            nullable=False,
        ),

        sa.Column(
            "s3_version_id",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "size_bytes",
            sa.BigInteger(),
            nullable=False,
        ),

        sa.Column(
            "content_type",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "etag",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["file_id"],
            ["files.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "bucket_name",
            "object_key",
            "s3_version_id",
            name="uq_file_version_s3_object",
        ),
    )

    # Create file_id index.
    op.create_index(
        "ix_file_versions_file_id",
        "file_versions",
        ["file_id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_file_versions_file_id",
        table_name="file_versions",
    )

    op.drop_table("file_versions")

    op.drop_index(
        "ix_files_status",
        table_name="files",
    )

    op.drop_column(
        "files",
        "upload_expires_at",
    )
