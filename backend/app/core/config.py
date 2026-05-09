from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    DISCORD_WEBHOOK_URL: str

    class Config:
        env_file = str(BASE_DIR / ".env")

settings = Settings()