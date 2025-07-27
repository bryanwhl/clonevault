"""
Post, Comment and Vote models for social feed
"""

from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Post(Base):
    """Post model for social feed"""
    
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(50), default="text")  # 'text', 'link', 'image', 'poll'
    tags = Column(ARRAY(Text))
    metadata = Column(JSON, default={})  # For links, images, poll options
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("PostVote", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title[:50]}, user_id={self.user_id})>"


class PostVote(Base):
    """Post vote model"""
    
    __tablename__ = "post_votes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vote_type = Column(String(10), nullable=False)  # 'up', 'down'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint to prevent duplicate votes
    __table_args__ = (UniqueConstraint('post_id', 'user_id', name='unique_post_vote'),)
    
    # Relationships
    post = relationship("Post", back_populates="votes")
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<PostVote(id={self.id}, post_id={self.post_id}, vote_type={self.vote_type})>"


class Comment(Base):
    """Comment model"""
    
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="SET NULL"))
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    is_edited = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent_comment = relationship("Comment", remote_side=[id])
    replies = relationship("Comment", back_populates="parent_comment")
    votes = relationship("CommentVote", back_populates="comment", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"


class CommentVote(Base):
    """Comment vote model"""
    
    __tablename__ = "comment_votes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vote_type = Column(String(10), nullable=False)  # 'up', 'down'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint to prevent duplicate votes
    __table_args__ = (UniqueConstraint('comment_id', 'user_id', name='unique_comment_vote'),)
    
    # Relationships
    comment = relationship("Comment", back_populates="votes")
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<CommentVote(id={self.id}, comment_id={self.comment_id}, vote_type={self.vote_type})>"