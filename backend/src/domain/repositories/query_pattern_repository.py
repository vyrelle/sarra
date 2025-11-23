
from abc import ABC, abstractmethod
from ..entities.query_pattern import QueryPattern

class IQueryPatternRepository(ABC):
    
    @abstractmethod
    async def get(self, query_hash: str) -> QueryPattern:
        pass

    @abstractmethod
    async def save(self, query_pattern: QueryPattern) -> None:
        pass
