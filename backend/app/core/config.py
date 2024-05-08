import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    access_secret_key: str = os.getenv("ACCESS_SECRET_KEY", "")
    refresh_secret_key: str = os.getenv("REFRESH_SECRET_KEY", "")


settings = Settings()
