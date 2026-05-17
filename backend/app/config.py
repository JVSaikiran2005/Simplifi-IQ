from pydantic import EmailStr, Field, AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    SENDGRID_API_KEY: str | None = Field(None, env="SENDGRID_API_KEY")
    RESEND_API_KEY: str | None = Field(None, env="RESEND_API_KEY")
    SENDGRID_FROM_EMAIL: EmailStr = Field(..., env="SENDGRID_FROM_EMAIL")
    SENDGRID_REPLY_TO: EmailStr | None = Field(None, env="SENDGRID_REPLY_TO")
    NEXT_PUBLIC_API_BASE_URL: str = Field("http://localhost:8000", env="NEXT_PUBLIC_API_BASE_URL")
    DATABASE_PATH: str = Field("./data/leads.db", env="DATABASE_PATH")
    REPORT_DIR: str = Field("./reports", env="REPORT_DIR")
    WEBSITE_TIMEOUT: int = Field(10, env="WEBSITE_TIMEOUT")
    OPENAI_MODEL: str = Field("gemini-1.5", env="OPENAI_MODEL")
    OPENAI_RETRY_COUNT: int = Field(2, env="OPENAI_RETRY_COUNT")
    OPENAI_MAX_TOKENS: int = Field(1200, env="OPENAI_MAX_TOKENS")
    GOOGLE_SERVICE_ACCOUNT_FILE: str | None = Field(None, env="GOOGLE_SERVICE_ACCOUNT_FILE")
    GOOGLE_SHEETS_ID: str | None = Field(None, env="GOOGLE_SHEETS_ID")
    GOOGLE_DRIVE_FOLDER_ID: str | None = Field(None, env="GOOGLE_DRIVE_FOLDER_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def email_provider(self) -> str:
        if self.SENDGRID_API_KEY:
            return "sendgrid"
        if self.RESEND_API_KEY:
            return "resend"
        return "none"


settings = Settings()
