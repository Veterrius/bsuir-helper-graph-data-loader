from ..schemas import CustomModel


class KnowledgeBaseModel(CustomModel):
    pass


class DataLoadingResult(KnowledgeBaseModel):
    status: str
    files_loaded: int
    saved_to_vector_store: bool