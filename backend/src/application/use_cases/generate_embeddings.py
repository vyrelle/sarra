
from dataclasses import dataclass
from ....domain.repositories.document_repository import IDocumentRepository
from ..services.embedding_service import IEmbeddingService

@dataclass
class GenerateEmbeddingsUseCase:
    document_repository: IDocumentRepository
    embedding_service: IEmbeddingService
    
    async def execute(self) -> None:
        documents = await self.document_repository.get_all()
        for doc in documents:
            if not doc.embedding:
                doc.embedding = await self.embedding_service.generate_embedding(doc.content)
                await self.document_repository.update(doc)
