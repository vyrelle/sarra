
import json
from sqlalchemy.orm import Session
from ....domain.entities.query_pattern import QueryPattern
from ....domain.repositories.query_pattern_repository import IQueryPatternRepository
from .models import QueryPattern as QueryPatternModel

class QueryPatternRepository(IQueryPatternRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get(self, query_hash: str) -> QueryPattern:
        query_pattern = self.db_session.query(QueryPatternModel).filter_by(query_hash=query_hash).first()
        if not query_pattern:
            return None
        
        # Deserialize successful_docs from JSON string
        query_pattern.successful_docs = json.loads(query_pattern.successful_docs)
        return QueryPattern(**query_pattern.__dict__)

    async def save(self, query_pattern: QueryPattern) -> None:
        query_pattern_model = self.db_session.query(QueryPatternModel).filter_by(query_hash=query_pattern.query_hash).first()
        
        # Serialize successful_docs to JSON string
        query_pattern_dict = query_pattern.__dict__
        query_pattern_dict['successful_docs'] = json.dumps(query_pattern_dict['successful_docs'])

        if not query_pattern_model:
            query_pattern_model = QueryPatternModel(**query_pattern_dict)
            self.db_session.add(query_pattern_model)
        else:
            for key, value in query_pattern_dict.items():
                setattr(query_pattern_model, key, value)
        self.db_session.commit()
