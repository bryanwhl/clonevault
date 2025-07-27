"""
Database connection and session management
"""

from typing import AsyncGenerator, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from supabase import create_client, Client

from app.core.config import get_settings

logger = structlog.get_logger(__name__)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass


class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.supabase_client: Optional[Client] = None
    
    async def connect(self):
        """Initialize database connections"""
        settings = get_settings()
        
        # SQLAlchemy async engine
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            future=True,
            pool_pre_ping=True,
        )
        
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        # Supabase client
        self.supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        
        logger.info("Database connections initialized")
    
    async def disconnect(self):
        """Close database connections"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connections closed")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session"""
        if not self.session_factory:
            raise RuntimeError("Database not initialized")
        
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    def get_supabase(self) -> Client:
        """Get Supabase client"""
        if not self.supabase_client:
            raise RuntimeError("Supabase client not initialized")
        return self.supabase_client


# Global database manager instance
database_manager = DatabaseManager()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    async for session in database_manager.get_session():
        yield session


def get_supabase() -> Client:
    """Dependency to get Supabase client"""
    return database_manager.get_supabase()