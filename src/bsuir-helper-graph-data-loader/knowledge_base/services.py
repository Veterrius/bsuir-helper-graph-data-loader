import asyncio
from typing import AsyncIterable, Set, AsyncGenerator
from abc import ABC, abstractmethod
from pathlib import Path

from llama_index.core import PropertyGraphIndex, Document
from llama_index.readers.file.markdown import MarkdownReader
from organisation_utils.logging_config import logger_factory

from ..models import FileData
from .config import settings
from .schemas import DataLoadingResult 


logger = logger_factory.get_logger("SERVICES LOGGER")


class DirectoryFileDataLoader(ABC):
    def __init__(
            self,
            root_directory_path: Path,
            index: PropertyGraphIndex,
            allowed_extentions: Set[str],
            embed_kg_nodes: bool = True,
            show_progress: bool = True,
    ) -> None:
        self.root_directory_path = root_directory_path
        self.index = index
        self.allowed_extentions = {ext.lower() for ext in allowed_extentions}
        self.embed_kg_nodes = embed_kg_nodes
        self.show_progress = show_progress
    
    @abstractmethod
    def read_file(self, file: FileData) -> AsyncGenerator[Document, None]:
        ...

    async def read_directory(self) -> AsyncIterable[FileData]:
        logger.info(f"Scanning storage directory: {self.root_directory_path}")
        for file_path in self.root_directory_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.allowed_extentions:
                try:
                    yield FileData.from_path(file_path, with_content=False)
                except ValueError as e:
                    logger.warning(
                        "Skipping file with invalid path structure:" + 
                        f"{file_path}. Error: {e}"
                    )
                except Exception as e:
                    logger.error(f"Failed to process path {file_path}: {e}",
                                  exc_info=True)

    async def load_files_into_storage(self) -> DataLoadingResult:
        logger.info("Started to load files into the knowledge base")
        files_processed = 0
        async for file_data in self.read_directory():
            logger.info(
                f"Processing file: {file_data.path.name}" +
                f"from url: {file_data.url}"
            )
            try:
                async for doc in self.read_file(file_data):
                    await self.index.ainsert(doc)
                files_processed += 1
                logger.info(
                    f"Successfully loaded {file_data.path.name} into index"
                )
            except Exception as e:
                logger.error(
                    f"Failed to load file {file_data.path.name}: {e}",
                    exc_info=True
                )
        logger.info(f"Finished loading. Total files: {files_processed}")
        if (self.embed_kg_nodes 
            and hasattr(self.index, 'vector_store') 
            and self.index.vector_store is not None
        ):
            logger.info(f"Persisting vector store")
            await asyncio.to_thread(
                self.index.vector_store.persist,
                persist_path=str(settings.VECTOR_STORE_PATH)
            )
        return DataLoadingResult(
            status="ok",
            files_loaded=files_processed,
            saved_to_vector_store=self.embed_kg_nodes
        )
    

class MarkdownFileDataLoader(DirectoryFileDataLoader):

    def __init__(
            self, 
            root_directory_path: Path, 
            index: PropertyGraphIndex, 
            embed_kg_nodes: bool = True, 
            show_progress: bool = True,
            remove_hyperlinks: bool = True,
            remove_images: bool = True,
            separator: str = " "
    ) -> None:
        markdown_extentions = {".md", ".markdown"}
        super().__init__(
            root_directory_path, 
            index, 
            markdown_extentions,
            embed_kg_nodes, 
            show_progress,
        )
        self.remove_hyperlinks = remove_hyperlinks
        self.remove_images = remove_images
        self.separator = separator

    async def read_file(self, file: FileData) -> AsyncGenerator[Document, None]:
        loader = MarkdownReader(
            self.remove_hyperlinks, 
            self.remove_images,
            self.separator
        )
        documents = await loader.aload_data(file.path)
        for doc in documents:
            doc.metadata["source_url"] = file.url
            doc.metadata["file_name"] = file.path.name
            yield doc
