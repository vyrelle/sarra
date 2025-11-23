
from abc import ABC, abstractmethod
from typing import List, Dict

class IChatService(ABC):
    
    @abstractmethod
    async def generate_answer(self, question: str, context: List[Dict]) -> str:
        pass
