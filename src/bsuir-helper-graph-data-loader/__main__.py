from fastapi import FastAPI

from .knowledge_base.router import router as kb_router
from .file.router import router as file_router 


app = FastAPI()
app.include_router(kb_router)
app.include_router(file_router)


@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}
