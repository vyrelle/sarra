
from abc import ABC, abstractmethod
from typing import List
from ..entities.feedback import Feedback

class IFeedbackRepository(ABC):
    
    @abstractmethod
    async def save(self, feedback: Feedback) -> None:
        pass
        
    @abstractmethod
    async def get_all(self) -> List[Feedback]:
        pass
