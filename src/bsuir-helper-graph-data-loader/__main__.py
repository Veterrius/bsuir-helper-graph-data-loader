from mimetypes import add_type

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .knowledge_base.router import router as kb_router
from .file.router import router as file_router 
from .utils import setup_llm_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    add_type("text/markdown", ".md")
    setup_llm_services()
    
    yield
    
    print("Application shutdown...")


app = FastAPI(title="Your Knowledge Base API", lifespan=lifespan)
app.include_router(kb_router)
app.include_router(file_router)


@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}
