
from dataclasses import dataclass
from typing import List, Dict
from ....domain.repositories.document_performance_repository import IDocumentPerformanceRepository
from ....domain.repositories.query_pattern_repository import IQueryPatternRepository
from ..services.query_transformation_service import IQueryTransformationService

@dataclass
class SubmitQueryUseCase:
    document_repository: IDocumentRepository
    embedding_service: IEmbeddingService
    chat_service: IChatService
    doc_perf_repo: IDocumentPerformanceRepository
    query_pattern_repo: IQueryPatternRepository
    query_transformation_service: IQueryTransformationService # Добавили новый сервис
    
    async def execute(self, question: str) -> Dict:
        # 1. Трансформация запроса с помощью маленькой модели
        hypothetical_answer = await self.query_transformation_service.generate_hypothetical_answer(question)
        enriched_query = f"{question}\n{hypothetical_answer}"

        # 2. Поиск по обогащенному запросу
        question_embedding = await self.embedding_service.generate_embedding(enriched_query)
        documents = await self.document_repository.find_by_embedding(question_embedding, 10) # Get more results for reranking
        
        # 3. Переранжирование с учетом фидбэка
        reranked_documents = await self._rerank_with_learning(question, documents)

        # 4. Генерация ответа с помощью основной, большой модели
        context = []
        for doc in reranked_documents[:3]: # Use top 3 after reranking
            context.append({"content": doc.content, "name": doc.name})
            
        answer = await self.chat_service.generate_answer(question, context)
        
        return {
            "answer": answer,
            "sources": [doc.__dict__ for doc in reranked_documents[:3]]
        }

    async def _rerank_with_learning(self, question: str, documents: List[Dict]) -> List[Dict]:
        for doc in documents:
            doc_perf = await self.doc_perf_repo.get(doc.id, question)
            if doc_perf:
                # Simple reranking: boost score by average rating
                # A more complex algorithm could be used here
                doc.score = doc.score * (1 + doc_perf.avg_rating / 5.0)
        
        return sorted(documents, key=lambda x: x.score, reverse=True)
