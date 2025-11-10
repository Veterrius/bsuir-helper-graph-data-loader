import os
from pathlib import Path
from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict

from .models import Extension, Url

class Settings(BaseSettings):
    UPLOAD_DIR: Path
    MAX_FILE_SIZE: int
    ALLOWED_EXTENSIONS: Set[Extension]
    MODEL_NAME: str
    EMBEDDINGS_MODEL_NAME: str
    OLLAMA_BASE_URL: Url = Url("http://localhost:11434")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
        extra="ignore",
    )


settings = Settings()