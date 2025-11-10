from .services import FileService
from .config import settings


def get_file_service() -> FileService:
    return FileService(
        settings.UPLOAD_DIR,
        settings.MAX_FILE_SIZE,
        settings.ALLOWED_EXTENSIONS
    )
