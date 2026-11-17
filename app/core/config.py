from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cloud File Storage"

    # Database
    database_url: str

    # AWS

    aws_region: str

    # S3
    s3_bucket_name: str

    # Cognito
    cognito_user_pool_id: str
    cognito_client_id: str
    cognito_client_secret: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()