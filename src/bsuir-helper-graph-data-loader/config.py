import os
from pathlib import Path
from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    UPLOAD_DIR: Path
    MAX_FILE_SIZE: int
    ALLOWED_EXTENSIONS: Set[str]
    MODEL_NAME: str
    EMBEDDINGS_MODEL_NAME: str
    NEBULA_SPACE_NAME: str
    VECTOR_STORE_PATH: str
    OVERWRITE_GRAPH_STORAGE: bool = False

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
        extra="ignore",
    )

    def get_model_name(self):
        return self.MODEL_NAME

    def get_embeddings_model_name(self):
        return self.EMBEDDINGS_MODEL_NAME
    

settings = Settings()