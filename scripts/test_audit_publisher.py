
from uuid import uuid4

from app.modules.audit.schemas.audit_event import AuditEvent
from app.modules.audit.constants import (
    AuditAction,
    AuditResourceType,
    AuditStatus,
    AuditSource,
)
from app.modules.audit.services.audit_publisher import AuditPublisher


event = AuditEvent(
    event_id=uuid4(),
    actor_id=None,
    action=AuditAction.REPORT_GENERATED,
    resource_type=AuditResourceType.REPORT,
    resource_id="reports/daily/test/storage-report.csv",
    status=AuditStatus.SUCCESS,
    source=AuditSource.SYSTEM,
    details={
        "filename": "storage-report.csv",
        "bucket": "harisreportbucket",
        "object_key": "reports/daily/test/storage-report.csv",
    },
)

message_id = AuditPublisher.publish(event)

print("Published successfully:", message_id)
