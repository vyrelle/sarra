
from typing import List
import json
from sqlalchemy.orm import Session
from ....domain.entities.document import Document
from ....domain.repositories.document_repository import IDocumentRepository
from .models import Document as DocumentModel

class DocumentRepository(IDocumentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def find_by_embedding(self, embedding: List[float], top_k: int) -> List[Document]:
        # This is a simplified example. In a real scenario, you would use a vector search extension like pgvector.
        documents = self.db_session.query(DocumentModel).limit(top_k).all()
        return [Document(
            id=doc.id,
            name=doc.name,
            content=doc.content,
            link=doc.egov_link,
            embedding=json.loads(doc.embedding) if doc.embedding else None
        ) for doc in documents]

        async def save(self, doc: Document) -> None:
        doc_model = DocumentModel(**doc.__dict__)
        self.db_session.add(doc_model)
        self.db_session.commit()

    async def get_all(self) -> List[Document]:
        documents = self.db_session.query(DocumentModel).all()
        return [Document(
            id=doc.id,
            name=doc.name,
            content=doc.content,
            link=doc.egov_link,
            embedding=json.loads(doc.embedding) if doc.embedding else None
        ) for doc in documents]

    async def update(self, doc: Document) -> None:
        doc_model = self.db_session.query(DocumentModel).filter(DocumentModel.id == doc.id).first()
        if doc_model:
            doc_model.embedding = json.dumps(doc.embedding)
            self.db_session.commit()

    async def get_by_id(self, doc_id: str) -> Document:
        doc = self.db_session.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if not doc:
            return None
        return Document(
            id=doc.id,
            name=doc.name,
            content=doc.content,
            link=doc.egov_link,
            embedding=json.loads(doc.embedding) if doc.embedding else None
        )
