from .services import FileService
from .config import settings


def get_file_service() -> FileService:
    return FileService(
        settings.get_upload_dir(),
        settings.get_max_file_size(),
        settings.get_allowed_extensions()
    )
