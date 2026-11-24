
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.modules.audit.constants import (
    AuditAction,
    AuditResourceType,
    AuditStatus,
    AuditSource,
)


class AuditEvent(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
    )

    event_id: UUID = Field(default_factory=uuid4)

    actor_id: UUID | None = None

    action: AuditAction

    resource_type: AuditResourceType

    resource_id: str | None = None

    status: AuditStatus

    source: AuditSource

    details: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
