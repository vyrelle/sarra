
import json
from dataclasses import dataclass
from ....domain.entities.document import Document
from ....domain.repositories.document_repository import IDocumentRepository

@dataclass
class LoadDocumentsUseCase:
    document_repository: IDocumentRepository

    async def execute(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            documents_data = json.load(f)
        
        for doc_data in documents_data:
            doc = Document(
                id=doc_data.get('id'),
                name=doc_data.get('name'),
                content=doc_data.get('chunks'),
                link=doc_data.get('eGov_link')
            )
            await self.document_repository.save(doc)
