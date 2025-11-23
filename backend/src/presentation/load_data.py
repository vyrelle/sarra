
import asyncio
from ..infrastructure.persistence.sqlalchemy.database import SessionLocal
from ..infrastructure.persistence.sqlalchemy.document_repository import DocumentRepository
from ..application.use_cases.load_documents import LoadDocumentsUseCase

async def main():
    db_session = SessionLocal()
    try:
        document_repository = DocumentRepository(db_session)
        load_documents_use_case = LoadDocumentsUseCase(document_repository)
        
        # Path to the data file
        file_path = "/home/user/feedback-rag-system/app/rag_documents.json"
        
        print(f"Loading documents from {file_path}...")
        await load_documents_use_case.execute(file_path)
        print("Documents loaded successfully.")
        
    finally:
        db_session.close()

if __name__ == "__main__":
    asyncio.run(main())
