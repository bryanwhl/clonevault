"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, agents, chat, feed, matches, notifications

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(feed.router, prefix="/feed", tags=["feed"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])