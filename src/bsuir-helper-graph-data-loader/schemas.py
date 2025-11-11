from datetime import datetime
from pathlib import Path

from pydantic import BaseModel


class CustomModel(BaseModel):
    pass


class FileInfo(CustomModel):
    name: str
    size: int
    content_type: str
    upload_time: datetime

    class Config:
        json_encoders = {
            Path: str
        }
