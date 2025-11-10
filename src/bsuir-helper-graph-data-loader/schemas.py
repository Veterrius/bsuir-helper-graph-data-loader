from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, field_validator
from config import settings


class CustomModel(BaseModel):
    pass


class FileInfo(CustomModel):
    name: str
    size: int
    content_type: str
    upload_time: datetime

    @field_validator("name")
    @classmethod
    def validate_extension(cls, v: str) -> str:
        suf = Path(v).suffix.lower()
        if suf and suf not in settings.get_all:
            raise ValueError(f"Extension {suf} not allowed")
        return v

    class Config:
        json_encoders = {
            Path: str
        }
