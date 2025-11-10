from __future__ import annotations
from mimetypes import guess_extension, guess_type

from pydantic import HttpUrl

from ..schemas import CustomModel
from ..models import FileData, Url, Extension


class FileModel(CustomModel):
    pass


class DocumentFile(FileModel):
    source_url: HttpUrl
    content_type: str
    content: str

    def to_file_data(self) -> FileData:
        return FileData(
            Url(str(self.source_url)),
            Extension(
                extension
                if (extension:=guess_extension(self.content_type)) is not None 
                else 'unknown'
            ),
            self.content.encode("utf-8")
        )
    
    @classmethod
    def from_file_data(cls, file_data: FileData) -> DocumentFile:
        return DocumentFile(
            source_url=HttpUrl(file_data.url),
            content_type=(
                content_type
                if (content_type:=guess_type(file_data.extension)[0]) is not None
                else 'unknown'
            ),
            content=(
                content.decode('utf-8')
                if (content:=file_data.content) is not None
                else ""
            )
        )
