
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Document:
    id: str
    name: str
    content: str
    link: Optional[str] = None
    embedding: Optional[List[float]] = None
