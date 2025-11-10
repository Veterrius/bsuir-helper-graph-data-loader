import os

from fastapi import Depends
from llama_index.core import PropertyGraphIndex
from llama_index.core.graph_stores import PropertyGraphStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.graph_stores.nebula import NebulaPropertyGraphStore
from llama_index.core.vector_stores.types import BasePydanticVectorStore

from .services import DirectoryFileDataLoader, MarkdownFileDataLoader
from .config import settings


def get_graph_store() -> PropertyGraphStore:
    return NebulaPropertyGraphStore(
        space=settings.NEBULA_SPACE_NAME,
        overwrite=settings.OVERWRITE_GRAPH_STORAGE
    )


def get_vector_store() -> BasePydanticVectorStore:
    vector_store_path = settings.VECTOR_STORE_PATH
    if os.path.exists(vector_store_path):
        return SimpleVectorStore.from_persist_path(str(vector_store_path))
    return SimpleVectorStore()


def get_index(
        graph_store: PropertyGraphStore = Depends(get_graph_store),
        vector_store: BasePydanticVectorStore = Depends(get_vector_store),
) -> PropertyGraphIndex:
    return PropertyGraphIndex(
        nodes=[],
        property_graph_store=graph_store,
        vector_store=vector_store
    )


def get_data_loader(
        index: PropertyGraphIndex = Depends(get_index)
) -> DirectoryFileDataLoader:
    return MarkdownFileDataLoader(
        root_directory_path=settings.UPLOAD_DIR,
        index=index,
        embed_kg_nodes=settings.EMBEDDINGS_MODEL_NAME is not None,
        show_progress=True,
        remove_hyperlinks=settings.MARKDOWN_REMOVE_HYPERLINKS,
        remove_images=settings.MARKDOWN_REMOVE_IMAGES,
        separator=settings.MARKDOWN_SEPARATOR
    )
