
from typing import List
from sqlalchemy.orm import Session
from ....domain.entities.feedback import Feedback
from ....domain.repositories.feedback_repository import IFeedbackRepository
from .models import Feedback as FeedbackModel

class FeedbackRepository(IFeedbackRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def save(self, feedback: Feedback) -> None:
        feedback_model = FeedbackModel(**feedback.__dict__)
        self.db_session.add(feedback_model)
        self.db_session.commit()

    async def get_all(self) -> List[Feedback]:
        feedbacks = self.db_session.query(FeedbackModel).all()
        return [Feedback(**fb.__dict__) for fb in feedbacks]
