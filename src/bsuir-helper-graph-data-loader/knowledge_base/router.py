from fastapi import Depends, APIRouter
from llama_index.core import PropertyGraphIndex

from .dependencies import get_data_loader, get_index
from .services import DirectoryFileDataLoader


router = APIRouter(prefix='/kb')


@router.post("/build", status_code=200)
async def build_knowledge_base(
    index: PropertyGraphIndex = Depends(get_index),
    loader: DirectoryFileDataLoader = Depends(get_data_loader)
):
    return await loader.load_files_into_storage(index)
