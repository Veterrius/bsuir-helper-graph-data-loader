from pathlib import Path
from typing import List

from ..models import FileData, Extension
from .config import settings


class FileService:
    def __init__(
        self, 
        upload_dir: Path | None = None,
        max_file_size: int | None = None, 
        allowed_extensions: set[Extension] | None = None
    ) -> None:
        self.upload_dir = (
            upload_dir
            if upload_dir is not None
            else settings.UPLOAD_DIR
        )
        self.max_file_size = (
            max_file_size
            if max_file_size is not None
            else settings.MAX_FILE_SIZE
        )
        self.allowed_extensions = (
            allowed_extensions
            if allowed_extensions is not None
            else settings.ALLOWED_EXTENSIONS
        )
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file_data: FileData) -> FileData:
        """Сохраняет загруженный файл и возвращает метаданные."""
        self.max_file_size
        if file_data.content is None:
            raise ValueError("File cannot be created. No content")
        if file_data.size > self.max_file_size:
            raise ValueError(
                f"File too large. Max size: {self.max_file_size // 1024} KB"
            )
        if file_data.extension not in self.allowed_extensions:
            raise ValueError("File extension not allowed")
        with open(self.upload_dir / file_data.path, 'wb') as file:
            file.write(file_data.content)
        return file_data

    def list_files(self, ext: Extension = Extension('.*')) -> List[FileData]:
        """Возвращает список всех файлов в директории с указаным расширением."""
        return [
            FileData.from_path(filepath) 
            for filepath in self.upload_dir.glob(f'*{ext}')
            if filepath.is_file()
        ]

    def get_file(self, filepath: Path) -> FileData:
        """Возвращает путь к файлу. Проверяет существование."""
        if not filepath.exists():
            raise FileNotFoundError("File not found")
        return FileData.from_path(filepath)

    def delete_file(self, filepath: Path) -> None:
        """Удаляет файл по имени."""
        (self.upload_dir / filepath).unlink()