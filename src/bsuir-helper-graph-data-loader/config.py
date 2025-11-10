import os
from pathlib import Path
from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict

from .models import Extension

class Settings(BaseSettings):
    UPLOAD_DIR: Path
    MAX_FILE_SIZE: int
    ALLOWED_EXTENSIONS: Set[Extension]
    MODEL_NAME: str
    EMBEDDINGS_MODEL_NAME: str
    NEBULA_SPACE_NAME: str
    VECTOR_STORE_PATH: Path
    OVERWRITE_GRAPH_STORAGE: bool = False
    MARKDOWN_REMOVE_HYPERLINKS: bool = True
    MARKDOWN_REMOVE_IMAGES: bool = True
    MARKDOWN_SEPARATOR: str = " "

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
        extra="ignore",
    )


settings = Settings()