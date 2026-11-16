
import base64
import hashlib
import hmac

from app.core.config import settings


def calculate_secret_hash(username: str) -> str | None:
    """
    Generate Cognito SECRET_HASH for an App Client
    configured with a client secret.
    """

    client_secret = settings.cognito_client_secret
    client_id = settings.cognito_client_id

    if not client_secret:
        return None

    message = username + client_id

    digest = hmac.new(
        key=client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    return base64.b64encode(digest).decode("utf-8")
