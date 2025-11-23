
from dataclasses import dataclass
import hashlib
from typing import List, Dict
from ....domain.entities.feedback import Feedback
from ....domain.repositories.document_performance_repository import IDocumentPerformanceRepository
from ....domain.repositories.query_pattern_repository import IQueryPatternRepository

@dataclass
class UpdateLearningMetricsUseCase:
    doc_perf_repo: IDocumentPerformanceRepository
    query_pattern_repo: IQueryPatternRepository

    async def execute(self, feedback: Feedback, retrieved_docs: List[Dict]):
        # Update document performance
        for doc in retrieved_docs:
            doc_perf = await self.doc_perf_repo.get(doc['id'], feedback.question)
            if not doc_perf:
                doc_perf = DocumentPerformance(doc_id=doc['id'], query_text=feedback.question)
            
            doc_perf.times_retrieved += 1
            if feedback.rating >= 4:
                doc_perf.positive_feedback += 1
            elif feedback.rating <= 2:
                doc_perf.negative_feedback += 1
            
            # Simplified avg rating calculation
            doc_perf.avg_rating = ((doc_perf.avg_rating * (doc_perf.times_retrieved -1)) + feedback.rating) / doc_perf.times_retrieved
            await self.doc_perf_repo.save(doc_perf)

        # Update query patterns
        query_hash = hashlib.md5(feedback.question.lower().encode()).hexdigest()
        query_pattern = await self.query_pattern_repo.get(query_hash)
        if not query_pattern:
            query_pattern = QueryPattern(query_hash=query_hash, query_text=feedback.question, successful_docs=[])
        
        query_pattern.usage_count += 1
        if feedback.rating >= 4:
            query_pattern.successful_docs.extend([doc['id'] for doc in retrieved_docs])
        
        query_pattern.avg_satisfaction = ((query_pattern.avg_satisfaction * (query_pattern.usage_count -1)) + feedback.rating) / query_pattern.usage_count
        await self.query_pattern_repo.save(query_pattern)
