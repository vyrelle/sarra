
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class DocumentPerformance(Base):
    __tablename__ = "document_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String)
    query_text = Column(Text)
    times_retrieved = Column(Integer, default=0)
    positive_feedback = Column(Integer, default=0)
    negative_feedback = Column(Integer, default=0)
    avg_rating = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.5)

class QueryPattern(Base):
    __tablename__ = "query_patterns"
    
    query_hash = Column(String, primary_key=True, index=True)
    query_text = Column(Text)
    successful_docs = Column(Text) # JSON string
    avg_satisfaction = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    content = Column(Text)
    egov_link = Column(String)
    embedding = Column(Text) # Store as string, convert in repository

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    question = Column(Text)
    answer = Column(Text)
    rating = Column(Integer)
    comment = Column(Text, nullable=True)
    is_validated = Column(Boolean, default=False)
