from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from dataclasses import dataclass
from typing import NewType, Tuple
from functools import reduce
from mimetypes import guess_type
from datetime import datetime

from .schemas import FileInfo
from .config import settings


Url = NewType('Url', str)
Sheme = NewType('Sheme', str)
Domain = NewType('Domain', str)
PathPart = NewType('PathPart', str)
Extension = NewType('Extension', str)


@dataclass
class FileData:
    DIR_SEP = '_'
    url: Url
    extension: Extension
    content: bytes | None = None

    @property
    def name(self) -> str:
        return str(hash(self.content))

    @property
    def size(self) -> int:
        if self.path.exists():
            return self.path.stat().st_size
        if self.content is not None:
            return len(
                self.content.encode() 
                if isinstance(self.content, str) 
                else self.content
            )
        return 0
    
    @property
    def path(self) -> Path:
        parsed_url = urlparse(self.url)
        domains = [self.DIR_SEP] + (
            parsed_url.hostname.split('.') 
            if parsed_url.hostname is not None 
            else []
        ) 
        dir_path = parsed_url.scheme / reduce(
            lambda x, y: y / x, 
            domains, 
            Path(parsed_url.path.strip('/'))
        )
        return (dir_path / self.name).with_suffix(self.extension)
    
    @classmethod
    def split_path_on_url_parts(
        cls, 
        path: Path
    ) -> Tuple[Sheme, Tuple[Domain, ...], Tuple[PathPart, ...]]:
        parts = path.parts
        if cls.DIR_SEP not in parts:
            raise ValueError(f'Invalid path: no sepration dir in {path}')
        sep_index = parts.index(cls.DIR_SEP)
        sep_next_index = sep_index + 1
        scheme = Sheme(parts[0])
        domains = tuple(map(Domain, parts[1:sep_index]))
        url_path_parts = (
            tuple() 
            if sep_next_index == len(parts) 
            else tuple((map(PathPart, parts[sep_next_index:])))
        )
        return scheme, domains, url_path_parts 
    
    @classmethod
    def get_url_from_path(cls, path: Path) -> Url:
        scheme, domains, url_path_parts = cls.split_path_on_url_parts(path)
        netloc = '.'.join(domains)
        url_path = '/' + '/'.join(url_path_parts)
        url = urlunparse((scheme, netloc, url_path, '', '', ''))
        return Url(url)

    @classmethod
    def from_path(cls, path: Path, with_content: bool = False) -> FileData:
        if with_content:
            with open(path, 'rb') as file:
                content = file.read()
        else:
            content = None
        url = cls.get_url_from_path(path) 
        return cls(
            url=Url(url),
            extension=Extension(path.suffix),
            content=content
        )
    
    @classmethod
    def from_file_info(cls, file_info: FileInfo) -> FileData:
        ...
    
    def to_file_info(self) -> FileInfo:
        return FileInfo(
            name=str(self.path),
            size=self.size,
            content_type=(
                content_type
                if (content_type:=guess_type(self.extension)[0]) is not None
                else 'unknown'
            ),
            upload_time=datetime.fromtimestamp(
                (settings.UPLOAD_DIR / self.path).stat().st_birthtime
            )
        )
