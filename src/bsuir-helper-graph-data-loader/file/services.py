from pathlib import Path
from typing import List
from organisation_utils.logging_config import logger_factory

from ..models import FileData, Extension
from .config import settings


logger = logger_factory.get_logger("FILE LOGGER")


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
            else set()
        )
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file_data: FileData) -> FileData:
        """Сохраняет загруженный файл и возвращает метаданные."""
        logger.info(f"Saving file {file_data.name}...")
        self.max_file_size
        if file_data.content is None:
            raise ValueError("File cannot be created. No content")
        if file_data.size > self.max_file_size:
            raise ValueError(
                f"File too large. Max size: {self.max_file_size // 1024} KB"
            )
        if file_data.extension not in self.allowed_extensions:
            raise ValueError("File extension not allowed")
        full_file_path = self.upload_dir / file_data.path
        parent_dir = full_file_path.parent
        parent_dir.mkdir(parents=True, exist_ok=True)
        with open(full_file_path, 'wb') as file:
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
