"""
Digital Twin Agent model
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Agent(Base):
    """Digital Twin Agent model"""
    
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    personality_type = Column(String(100))  # e.g., "professional", "casual", "technical"
    persona_description = Column(Text)
    conversation_style = Column(
        JSON,
        default={"tone": "professional", "enthusiasm_level": 7, "technical_depth": 5}
    )
    background_context = Column(Text)  # Parsed from resume
    goals = Column(ARRAY(Text))
    interests = Column(ARRAY(Text))
    is_active = Column(Boolean, default=True)
    last_conversation_at = Column(DateTime(timezone=True))
    total_conversations = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="agents")
    
    def __repr__(self) -> str:
        return f"<Agent(id={self.id}, name={self.name}, user_id={self.user_id})>"