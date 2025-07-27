"""
Embedding model for vector similarity search
"""

from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from app.core.database import Base


class Embedding(Base):
    """Embedding model for vector similarity search"""
    
    __tablename__ = "embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(50), nullable=False)  # 'user_profile', 'resume', 'post', 'agent'
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    embedding = Column(Vector(1536))  # OpenAI ada-002 embedding dimension
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Embedding(id={self.id}, entity_type={self.entity_type}, entity_id={self.entity_id})>"