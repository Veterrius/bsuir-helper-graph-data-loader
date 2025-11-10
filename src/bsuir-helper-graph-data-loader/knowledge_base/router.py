import os
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, APIRouter, HTTPException

from .schemas import DataLoadingResult
from .dependencies import get_vector_store, get_index


router = APIRouter(prefix='/kb')


@router.post("/build", status_code=200)
async def build_knowledge_base(index = Depends(get_index)):
    ...
