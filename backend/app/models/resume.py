"""
Resume model
"""

from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Resume(Base):
    """Resume model"""
    
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    parsed_data = Column(JSON, nullable=False)  # Structured resume data from parser
    raw_text = Column(Text)
    is_current = Column(Boolean, default=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    
    def __repr__(self) -> str:
        return f"<Resume(id={self.id}, user_id={self.user_id}, file_name={self.file_name})>"