"""
Redis connection and utilities
"""

from typing import Optional
import redis.asyncio as redis
import structlog

from app.core.config import get_settings

logger = structlog.get_logger(__name__)


class RedisManager:
    """Redis connection manager"""
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Initialize Redis connection"""
        settings = get_settings()
        
        try:
            self.client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            
            # Test connection
            await self.client.ping()
            logger.info("Redis connected successfully")
            
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            raise
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            logger.info("Redis disconnected")
    
    def get_client(self) -> redis.Redis:
        """Get Redis client"""
        if not self.client:
            raise RuntimeError("Redis not connected")
        return self.client


# Global Redis manager instance
redis_manager = RedisManager()


async def get_redis() -> redis.Redis:
    """Dependency to get Redis client"""
    return redis_manager.get_client()