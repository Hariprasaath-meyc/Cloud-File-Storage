
from botocore.exceptions import BotoCoreError, ClientError
import logging

from app.core.config import settings
from app.core.decorators.auth_decorators import handle_cognito_errors
from app.core.exceptions import AuthenticationException,  ExternalServiceException, InvalidRequestException
from app.modules.auth.schemas import LoginRequest, LoginResponse, PasswordChangeRequest
from app.modules.auth.utils import calculate_secret_hash


logger = logging.getLogger(__name__)
class AuthService:

    def __init__(self, cognito):
        self.cognito = cognito
        
    @handle_cognito_errors("login")
    def login(self, payload: LoginRequest) -> LoginResponse:
        email = str(payload.email)

        # Stage 2: Complete the password challenge
        if payload.session:
            if not payload.new_password:
                raise InvalidRequestException(
                    message="New password is required.",
                    error_code="NEW_PASSWORD_REQUIRED",
                )

            challenge_responses = {
                "USERNAME": email,
                "NEW_PASSWORD": payload.new_password,
            }

            secret_hash = calculate_secret_hash(email)
            if secret_hash:
                challenge_responses["SECRET_HASH"] = secret_hash

            response = self.cognito.respond_to_auth_challenge(
                ClientId=settings.cognito_client_id,
                ChallengeName="NEW_PASSWORD_REQUIRED",
                Session=payload.session,
                ChallengeResponses=challenge_responses,
            )

        # Stage 1: Initial login
        else:
            if not payload.password:
                raise InvalidRequestException(
                    message="Password is required.",
                    error_code="PASSWORD_REQUIRED",
                )

            auth_parameters = {
                "USERNAME": email,
                "PASSWORD": payload.password,
            }

            secret_hash = calculate_secret_hash(email)
            if secret_hash:
                auth_parameters["SECRET_HASH"] = secret_hash

            response = self.cognito.initiate_auth(
                ClientId=settings.cognito_client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters=auth_parameters,
            )

        # Cognito requires another authentication step
        if "ChallengeName" in response:
            challenge_name = response["ChallengeName"]

            return LoginResponse(
                message=(
                    "A password change is required."
                    if challenge_name == "NEW_PASSWORD_REQUIRED"
                    else "Additional authentication is required."
                ),
                challenge_required=True,
                challenge_name=challenge_name,
                session=response.get("Session"),
            )

        return self._build_token_response(response)


    @handle_cognito_errors("password_change")
    def complete_password_change(
        self,
        payload: PasswordChangeRequest,
    ) -> LoginResponse:

        email = str(payload.email)

        challenge_responses = {
            "USERNAME": email,
            "NEW_PASSWORD": payload.new_password,
        }

        secret_hash = calculate_secret_hash(email)
        if secret_hash:
            challenge_responses["SECRET_HASH"] = secret_hash

        response = self.cognito.respond_to_auth_challenge(
            ClientId=settings.cognito_client_id,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            Session=payload.session,
            ChallengeResponses=challenge_responses,
        )

        if "ChallengeName" in response:
            return LoginResponse(
                message="Additional authentication is required.",
                challenge_required=True,
                challenge_name=response["ChallengeName"],
                session=response.get("Session"),
            )

        return self._build_token_response(response)

    @staticmethod
    def _build_token_response(response: dict) -> LoginResponse:
        result = response.get("AuthenticationResult", {})

        if not result:
            raise ExternalServiceException(
                message="Authentication service returned an unexpected response.",
                error_code="INVALID_AUTHENTICATION_RESPONSE",
            )

        return LoginResponse(
            message="Login successful.",
            access_token=result.get("AccessToken"),
            id_token=result.get("IdToken"),
            refresh_token=result.get("RefreshToken"),
            token_type=result.get("TokenType"),
            expires_in=result.get("ExpiresIn"),
        )

    