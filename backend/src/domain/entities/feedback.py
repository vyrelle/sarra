
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Feedback:
    id: str
    user_id: str
    question: str
    answer: str
    rating: int
    comment: Optional[str] = None
    is_validated: bool = False
