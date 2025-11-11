from llama_index.core import Settings as LlamaSettings # Переименовываем, чтобы не путать
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from organisation_utils.logging_config import logger_factory

from .config import settings


logger = logger_factory.get_logger(__name__)

def setup_llm_services():

    logger.info("Setting up LLM and Embedding models...")

    embed_model = OllamaEmbedding(
        model_name=settings.EMBEDDINGS_MODEL_NAME,
        base_url=str(settings.OLLAMA_BASE_URL),
    )
    
    llm = Ollama(
        model=settings.MODEL_NAME,
        base_url=str(settings.OLLAMA_BASE_URL),
    )
    
    LlamaSettings.llm = llm
    LlamaSettings.embed_model = embed_model

    logger.info(
        f"LLM ('{settings.MODEL_NAME}') and "
        f"Embedding model ('{settings.EMBEDDINGS_MODEL_NAME}') have been configured globally."
    )