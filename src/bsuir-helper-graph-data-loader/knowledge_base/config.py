from pathlib import Path

from ..config import Settings


class KnowledgeBaseSettings(Settings):
    NEBULA_SPACE_NAME: str
    VECTOR_STORE_PATH: Path
    OVERWRITE_GRAPH_STORAGE: bool = False
    MARKDOWN_REMOVE_HYPERLINKS: bool = True
    MARKDOWN_REMOVE_IMAGES: bool = True
    MARKDOWN_SEPARATOR: str = " "


settings = KnowledgeBaseSettings()