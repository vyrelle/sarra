
from abc import ABC, abstractmethod
from typing import List
from ..entities.document import Document

class IDocumentRepository(ABC):
    
    @abstractmethod
    async def find_by_embedding(self, embedding: List[float], top_k: int) -> List[Document]:
        pass
        
    @abstractmethod
        @abstractmethod
    async def save(self, doc: Document) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[Document]:
        pass

    @abstractmethod
    async def update(self, doc: Document) -> None:
        pass

    async def get_by_id(self, doc_id: str) -> Document:
        pass
