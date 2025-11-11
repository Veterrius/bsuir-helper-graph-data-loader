from fastapi import Depends

from ..knowledge_base.dependencies import get_data_loader, DirectoryFileDataLoader
from .services import FileService
from .config import settings


def get_file_service(
    data_loader: DirectoryFileDataLoader = Depends(get_data_loader)
) -> FileService:
    return FileService(
        settings.UPLOAD_DIR,
        settings.MAX_FILE_SIZE,
        data_loader.allowed_extentions
    )
