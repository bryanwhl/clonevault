"""
Digital Twin Social Media Platform - FastAPI Main Application
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GzipMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.config import get_settings
from app.core.database import database_manager
from app.core.exceptions import setup_exception_handlers
from app.core.logging import setup_logging
from app.api.v1.api import api_router

# Setup structured logging
logger = structlog.get_logger(__name__)

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager"""
    settings = get_settings()
    
    logger.info("Starting Digital Twin Social Media Platform API")
    
    try:
        # Initialize database connection
        await database_manager.connect()
        logger.info("Database connected successfully")
        
        # Initialize Redis connection (if needed)
        # await redis_manager.connect()
        
        yield
        
    except Exception as e:
        logger.error("Failed to start application", error=str(e))
        raise
    finally:
        # Cleanup connections
        await database_manager.disconnect()
        logger.info("Database disconnected")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    # Setup logging first
    setup_logging(settings.log_level)
    
    app = FastAPI(
        title="Digital Twin Social Media Platform API",
        description="Backend service for AI-powered agent networking and social interactions",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )
    
    # Setup rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Add middleware
    app.add_middleware(GzipMiddleware, minimum_size=1000)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "service": "digital-twin-api"}
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Digital Twin Social Media Platform API",
            "version": "1.0.0",
            "docs": "/docs",
        }
    
    return app


# Create the application instance
app = create_application()

if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )