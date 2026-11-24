
import json
import logging

import boto3

from app.core.config import settings
from app.modules.audit.schemas.audit_event import AuditEvent

logger = logging.getLogger(__name__)

sns_client = boto3.client(
    "sns",
    region_name=settings.aws_region,
)


class AuditPublisher:

    @staticmethod
    def publish(event: AuditEvent) -> str:

        response = sns_client.publish(
            TopicArn=settings.sns_audit_topic_arn,
            Message=json.dumps(
                event.model_dump(mode="json")
            ),
            Subject=f"Audit Event: {event.action}",
        )

        message_id = response["MessageId"]

        logger.info(
            "Audit event published successfully",
            extra={
                "event_id": str(event.event_id),
                "message_id": message_id,
                "action": str(event.action),
            },
        )

        return message_id
