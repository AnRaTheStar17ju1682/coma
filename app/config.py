from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Optional


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    ENGINE_ECHO: bool
    LOGGING_LEVEL: int
    IMAGE_SALT: str
    CONTENT_DIR: str
    LOGS_DIR: str
    DEFAULT_IMAGES_QUALITY: int
    DEFAULT_RESIZE_RESOLUTION: Optional[tuple[int, int]]
    REDIS: str
    REDIS_FILES: str
    
    
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
    @field_validator("DEFAULT_RESIZE_RESOLUTION", mode="before")
    @classmethod
    def parse_resolution(cls, value: str | None):
        if value == "None":
            return None
        else:
            return tuple(int(_) for _ in value.split("_"))
    
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()