
from sqlalchemy.orm import Session
from ....domain.entities.document_performance import DocumentPerformance
from ....domain.repositories.document_performance_repository import IDocumentPerformanceRepository
from .models import DocumentPerformance as DocumentPerformanceModel

class DocumentPerformanceRepository(IDocumentPerformanceRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get(self, doc_id: str, query_text: str) -> DocumentPerformance:
        doc_perf = self.db_session.query(DocumentPerformanceModel).filter_by(doc_id=doc_id, query_text=query_text).first()
        if not doc_perf:
            return None
        return DocumentPerformance(**doc_perf.__dict__)

    async def save(self, doc_performance: DocumentPerformance) -> None:
        doc_perf_model = self.db_session.query(DocumentPerformanceModel).filter_by(doc_id=doc_performance.doc_id, query_text=doc_performance.query_text).first()
        if not doc_perf_model:
            doc_perf_model = DocumentPerformanceModel(**doc_performance.__dict__)
            self.db_session.add(doc_perf_model)
        else:
            for key, value in doc_performance.__dict__.items():
                setattr(doc_perf_model, key, value)
        self.db_session.commit()
