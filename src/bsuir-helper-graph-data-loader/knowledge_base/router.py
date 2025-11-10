from fastapi import Depends, APIRouter

from .dependencies import get_data_loader
from .services import DirectoryFileDataLoader


router = APIRouter(prefix='/kb')


@router.post("/build", status_code=200)
async def build_knowledge_base(
    loader: DirectoryFileDataLoader = Depends(get_data_loader)
):
    return await loader.load_files_into_storage()
