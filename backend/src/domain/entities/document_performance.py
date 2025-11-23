
from dataclasses import dataclass

@dataclass
class DocumentPerformance:
    doc_id: str
    query_text: str
    times_retrieved: int = 0
    positive_feedback: int = 0
    negative_feedback: int = 0
    avg_rating: float = 0.0
    relevance_score: float = 0.5
