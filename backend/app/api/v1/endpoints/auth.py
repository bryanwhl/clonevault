"""
Authentication endpoints
"""

from datetime import timedelta
from typing import Dict, Any

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import create_access_token, verify_google_token, get_current_active_user
from app.services.user_service import UserService

logger = structlog.get_logger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class GoogleAuthRequest(BaseModel):
    """Google OAuth token request"""
    google_token: str


class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]


class UserInfo(BaseModel):
    """User information response"""
    id: str
    email: EmailStr
    full_name: str
    profile_picture_url: str = None
    created_at: str


@router.post("/google", response_model=TokenResponse)
@limiter.limit("5/minute")
async def google_auth(
    auth_request: GoogleAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user with Google OAuth token
    """
    try:
        # Verify Google token and get user info
        google_user_info = await verify_google_token(auth_request.google_token)
        
        # Get or create user
        user_service = UserService(db)
        user = await user_service.get_or_create_user_from_google(google_user_info)
        
        # Create access token
        settings = get_settings()
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "name": user.full_name
            },
            expires_delta=access_token_expires
        )
        
        logger.info(
            "User authenticated successfully",
            user_id=str(user.id),
            email=user.email
        )
        
        return TokenResponse(
            access_token=access_token,
            expires_in=settings.access_token_expire_minutes * 60,
            user={
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "profile_picture_url": user.profile_picture_url,
                "created_at": user.created_at.isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Authentication failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


@router.post("/refresh")
@limiter.limit("10/minute")
async def refresh_token(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Refresh access token for authenticated user
    """
    try:
        settings = get_settings()
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        
        access_token = create_access_token(
            data={
                "sub": current_user["user_id"],
                "email": current_user["email"],
                "name": current_user["name"]
            },
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60
        }
        
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user information
    """
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(current_user["user_id"])
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserInfo(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            profile_picture_url=user.profile_picture_url,
            created_at=user.created_at.isoformat()
        )
        
    except Exception as e:
        logger.error("Failed to get user info", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )


@router.post("/logout")
async def logout(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Logout current user (client-side token invalidation)
    """
    logger.info("User logged out", user_id=current_user["user_id"])
    
    return {"message": "Successfully logged out"}