# backend/src/application/services/query_transformation_service.py
from abc import ABC, abstractmethod

class IQueryTransformationService(ABC):
    @abstractmethod
    async def generate_hypothetical_answer(self, query: str) -> str:
        """Generates a hypothetical answer for a query to enrich it."""
        pass
