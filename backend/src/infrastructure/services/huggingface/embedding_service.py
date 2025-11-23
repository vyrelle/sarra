
from typing import List
from sentence_transformers import SentenceTransformer
from ....application.services.embedding_service import IEmbeddingService

class EmbeddingService(IEmbeddingService):
    def __init__(self, model_name: str = 'BAAI/bge-m3'):
        self.model = SentenceTransformer(model_name)

    async def generate_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()
