from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model: str = "groq:llama-3.3-70b-versatile"
    database_url: str
    groq_api_key: str | None = None
    deepgram_api_key: str | None = None
    vobiz_public_url: str | None = None
    vobiz_auth_id: str | None = None
    vobiz_auth_token: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore",
    )

settings = Settings()