# All get_<smth>() functions are here
import os
from platform import node
from fastapi import Depends
from llama_index.core import PropertyGraphIndex
from llama_index.core.graph_stores import PropertyGraphStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.graph_stores.nebula import NebulaPropertyGraphStore
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from ..config import Settings, settings


def get_settings() -> Settings:
    return settings


def get_graph_store(
        current_settings: Settings = Depends(get_settings)
) -> PropertyGraphStore:
    ...


def get_vector_store(
        current_settings: Settings = Depends(get_settings)
) -> BasePydanticVectorStore:
    ...


def get_index(
        graph_store: PropertyGraphStore = Depends(get_graph_store),
        vector_store: BasePydanticVectorStore = Depends(get_vector_store),
) -> PropertyGraphIndex:
    ...
