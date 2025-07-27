"""
Match model for agent-driven user matching
"""

from datetime import datetime, timedelta
import uuid
from decimal import Decimal

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, CheckConstraint, UniqueConstraint, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Match(Base):
    """Match model for agent-driven user matching"""
    
    __tablename__ = "matches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    agent1_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    agent2_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"))
    match_reason = Column(Text)
    similarity_score = Column(DECIMAL(3, 2))  # 0.00 to 1.00
    status = Column(String(50), default="pending")  # 'pending', 'accepted', 'rejected', 'expired'
    user1_response = Column(String(20))  # 'accept', 'reject'
    user2_response = Column(String(20))  # 'accept', 'reject'
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.utcnow() + timedelta(days=7))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True))
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='unique_user_match'),
        CheckConstraint('user1_id < user2_id', name='check_user_order'),
        CheckConstraint(
            "status IN ('pending', 'accepted', 'rejected', 'expired')",
            name='check_match_status'
        ),
        CheckConstraint(
            "user1_response IN ('accept', 'reject') OR user1_response IS NULL",
            name='check_user1_response'
        ),
        CheckConstraint(
            "user2_response IN ('accept', 'reject') OR user2_response IS NULL",
            name='check_user2_response'
        )
    )
    
    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    agent1 = relationship("Agent", foreign_keys=[agent1_id])
    agent2 = relationship("Agent", foreign_keys=[agent2_id])
    conversation = relationship("Conversation")
    
    def __repr__(self) -> str:
        return f"<Match(id={self.id}, user1_id={self.user1_id}, user2_id={self.user2_id}, status={self.status})>"