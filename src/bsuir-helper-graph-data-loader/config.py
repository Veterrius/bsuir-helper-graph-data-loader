import os
from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    UPLOAD_DIR: Path
    MAX_FILE_SIZE: int
    MODEL_NAME: str
    EMBEDDINGS_MODEL_NAME: str
    OLLAMA_BASE_URL: HttpUrl = HttpUrl("http://localhost:11434")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
        extra="ignore",
    )


settings = Settings()