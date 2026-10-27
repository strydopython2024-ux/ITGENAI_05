from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_DIR = BASE_DIR / "DATA_BASE"
DATABASE_PATH = DATABASE_DIR / "investment.db"
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "Investment Guidance AI"
    app_version: str = "3.0.0"
    debug: bool = True

    jwt_secret_key: str = "dev-only-change-this-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Lightweight Gemini model. One model only; no fallback model.
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
