import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    cdse_user: str = os.getenv("CDSE_USER", "")
    cdse_pass: str = os.getenv("CDSE_PASS", "")
    storage_root: str = os.getenv("STORAGE_ROOT", "storage")

settings = Settings()
