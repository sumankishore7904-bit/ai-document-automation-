import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
