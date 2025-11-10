from pydantic import HttpUrl

from ..schemas import CustomModel


class FileModel(CustomModel):
    pass


class BaseDocument(FileModel):
    pass


class MarkdownDocument(BaseDocument):
    source_url: HttpUrl
    content: str
