
from dataclasses import dataclass
from typing import List

@dataclass
class QueryPattern:
    query_hash: str
    query_text: str
    successful_docs: List[str]
    avg_satisfaction: float = 0.0
    usage_count: int = 0
