
from abc import ABC, abstractmethod
from ..entities.document_performance import DocumentPerformance

class IDocumentPerformanceRepository(ABC):
    
    @abstractmethod
    async def get(self, doc_id: str, query_text: str) -> DocumentPerformance:
        pass

    @abstractmethod
    async def save(self, doc_performance: DocumentPerformance) -> None:
        pass
