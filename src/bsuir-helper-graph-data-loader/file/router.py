from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from fastapi.responses import FileResponse

from schemas import FileInfo
from .services import FileService
from .dependencies import get_file_service

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("", response_model=FileInfo, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...), 
    file_service: FileService = Depends(get_file_service)
):
    try:
        return file_service.save_file(file)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )


@router.get("", response_model=list[FileInfo])
async def list_files(file_service: FileService = Depends(get_file_service)):
    return file_service.list_files()


@router.get("/{filename}")
async def download_file(
    filename: str, 
    file_service: FileService = Depends(get_file_service)
):
    try:
        filepath = file_service.get_file_path(filename)
        return FileResponse(filepath, filename=filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    filename: str, 
    file_service: FileService = Depends(get_file_service)
):
    try:
        file_service.delete_file(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")