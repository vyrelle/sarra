
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from ....application.use_cases.submit_query import SubmitQueryUseCase
from ....application.use_cases.submit_feedback import SubmitFeedbackUseCase
from ....infrastructure.persistence.sqlalchemy.database import get_db, SessionLocal
from ....infrastructure.persistence.sqlalchemy.document_repository import DocumentRepository
from ....infrastructure.persistence.sqlalchemy.feedback_repository import FeedbackRepository
from ....infrastructure.services.huggingface.embedding_service import EmbeddingService
from ....infrastructure.services.huggingface.chat_service import ChatService

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Список разрешенных источников (доменов)
origins = [
    "https://sarra.live",      # Ваш основной домен
    "https://www.sarra.live",  # С префиксом www
    "http://localhost:5173", # Для локальной разработки (если нужно)
    "http://127.0.0.1:5500", # Для Live Server
    "null",                  # Для локальных HTML файлов
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Разрешаем все методы (GET, POST, etc.)
    allow_headers=["*"], # Разрешаем все заголовки
)

def get_submit_query_use_case(db: Session = Depends(get_db)) -> SubmitQueryUseCase:
    return SubmitQueryUseCase(
        document_repository=DocumentRepository(db),
        embedding_service=EmbeddingService(),
        chat_service=ChatService(),
        doc_perf_repo=DocumentPerformanceRepository(db),
        query_pattern_repo=QueryPatternRepository(db),
        query_transformation_service=HfQueryTransformationService() # <--- Добавили новый сервис
    )

def get_submit_feedback_use_case(db: Session = Depends(get_db)) -> SubmitFeedbackUseCase:
    return SubmitFeedbackUseCase(
        feedback_repository=FeedbackRepository(db)
    )

@app.post("/query")
async def submit_query(question: str, use_case: SubmitQueryUseCase = Depends(get_submit_query_use_case)):
    return await use_case.execute(question)

from ....application.use_cases.generate_embeddings import GenerateEmbeddingsUseCase

def get_generate_embeddings_use_case(db: Session = Depends(get_db)) -> GenerateEmbeddingsUseCase:
    return GenerateEmbeddingsUseCase(
        document_repository=DocumentRepository(db),
        embedding_service=EmbeddingService()
    )

@app.post("/embeddings/generate")
async def generate_embeddings(use_case: GenerateEmbeddingsUseCase = Depends(get_generate_embeddings_use_case)):
    await use_case.execute()
    return {"status": "embedding generation complete"}

from pydantic import BaseModel, Field
from typing import List, Dict, Any

class FeedbackRequest(BaseModel):
    id: str
    user_id: str
    question: str
    answer: str
    rating: int
    comment: str | None = None
    retrieved_docs: List[Dict[str, Any]] = Field(default_factory=list)

@app.post("/feedback")
async def submit_feedback(feedback_data: FeedbackRequest, use_case: SubmitFeedbackUseCase = Depends(get_submit_feedback_use_case)):
    await use_case.execute(feedback_data.dict())
    return {"status": "feedback received"}
