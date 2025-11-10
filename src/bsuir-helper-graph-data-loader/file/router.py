from pathlib import Path

from fastapi import APIRouter, HTTPException, status, Depends

from ..schemas import FileInfo
from .schemas import DocumentFile
from .services import FileService
from .dependencies import get_file_service


router = APIRouter(prefix="/files", tags=["Files"])


@router.post("", response_model=FileInfo, status_code=status.HTTP_201_CREATED)
async def create_file(
    file: DocumentFile, 
    file_service: FileService = Depends(get_file_service)
) -> FileInfo:
    try:
        return file_service.save_file(file.to_file_data()).to_file_info()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)   
        )


@router.get("", response_model=list[FileInfo])
async def list_files(
    file_service: FileService = Depends(get_file_service)
) -> list[FileInfo]:
    return [file_data.to_file_info() for file_data in file_service.list_files()]


@router.get("/{filepath}", response_model=FileInfo)
async def get_file(
    filename: str, 
    file_service: FileService = Depends(get_file_service)
):
    try:
        return file_service.get_file(Path(filename))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    filename: str, 
    file_service: FileService = Depends(get_file_service)
):
    try:
        file_service.delete_file(Path(filename))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")