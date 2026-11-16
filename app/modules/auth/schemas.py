
from pydantic import BaseModel, EmailStr, model_validator
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr

    # Initial login with temporary or permanent password
    password: str | None = None

    # Complete NEW_PASSWORD_REQUIRED challenge
    new_password: str | None = None
    session: str | None = None

    @model_validator(mode="after")
    def validate_login_request(self):
        if self.session:
            if not self.new_password:
                raise ValueError(
                    "New password is required when completing a challenge."
                )

            if self.password:
                raise ValueError(
                    "Do not provide the temporary password when completing a challenge."
                )

        elif not self.password:
            raise ValueError("Password is required.")

        return self


class LoginResponse(BaseModel):
    message: str
    challenge_required: bool = False
    challenge_name: str | None = None
    session: str | None = None

    access_token: str | None = None
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None


class PasswordChangeRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=8)
    session: str = Field(min_length=1)