import logging

import jwt
from jwt import PyJWKClient, PyJWTError

from app.core.config import settings
from app.core.exceptions import AuthenticationException


logger = logging.getLogger(__name__)

COGNITO_ISSUER = (
    f"https://cognito-idp.{settings.aws_region}.amazonaws.com/"
    f"{settings.cognito_user_pool_id}"
)

JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

jwks_client = PyJWKClient(JWKS_URL)


def verify_access_token(token: str) -> dict:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=COGNITO_ISSUER,
            options={
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": False,
            },
        )

        if claims.get("token_use") != "access":
            raise AuthenticationException(
                message="Invalid token type.",
                error_code="INVALID_TOKEN_TYPE",
            )

        if claims.get("client_id") != settings.cognito_client_id:
            raise AuthenticationException(
                message="Invalid application client.",
                error_code="INVALID_TOKEN_CLIENT",
            )

        return claims

    except AuthenticationException:
        raise

    except Exception as exc:
        logger.warning("Access token verification failed: %s", exc)

        raise AuthenticationException(
            message="Invalid or expired access token.",
            error_code="INVALID_ACCESS_TOKEN",
        ) from exc