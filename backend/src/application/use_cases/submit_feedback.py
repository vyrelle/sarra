
from dataclasses import dataclass
from ....domain.entities.feedback import Feedback
from ....domain.repositories.document_performance_repository import IDocumentPerformanceRepository
from ....domain.repositories.query_pattern_repository import IQueryPatternRepository
from .update_learning_metrics import UpdateLearningMetricsUseCase

@dataclass
class SubmitFeedbackUseCase:
    feedback_repository: IFeedbackRepository
    doc_perf_repo: IDocumentPerformanceRepository
    query_pattern_repo: IQueryPatternRepository
    
    async def execute(self, feedback_data: dict) -> None:
        feedback = Feedback(
            id=feedback_data.get('id'),
            user_id=feedback_data.get('user_id'),
            question=feedback_data.get('question'),
            answer=feedback_data.get('answer'),
            rating=feedback_data.get('rating'),
            comment=feedback_data.get('comment')
        )
        await self.feedback_repository.save(feedback)
        
        update_learning_metrics_use_case = UpdateLearningMetricsUseCase(
            doc_perf_repo=self.doc_perf_repo,
            query_pattern_repo=self.query_pattern_repo
        )
        await update_learning_metrics_use_case.execute(feedback, feedback_data.get('retrieved_docs', []))
