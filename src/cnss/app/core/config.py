from os import getenv
from pathlib import Path
import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

BASE_DIR = Path(__file__).parent.parent
DEV_MODE = getenv("DEV_MODE", "true").strip().lower() in {"1", "true", "yes"}

class Settings(BaseSettings):
    DB_NAME: str = "testdb"
    DB_USER: str = "testuser"
    DB_PASSWORD: str = "testpass"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

DB_URL: str = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"