"""
User management endpoints
"""

from typing import Dict, Any, List, Optional
import uuid

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel, EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.services.user_service import UserService

logger = structlog.get_logger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class UserProfileUpdate(BaseModel):
    """User profile update request"""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website_url: Optional[str] = None


class UserProfileResponse(BaseModel):
    """User profile response"""
    id: str
    email: EmailStr
    full_name: str
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website_url: Optional[str] = None
    privacy_settings: Dict[str, Any]
    is_active: bool
    created_at: str
    updated_at: str


class PrivacySettingsUpdate(BaseModel):
    """Privacy settings update request"""
    profile_visible: Optional[bool] = None
    agent_conversations_visible: Optional[bool] = None


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's profile
    """
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(current_user["user_id"])
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfileResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            profile_picture_url=user.profile_picture_url,
            bio=user.bio,
            location=user.location,
            linkedin_url=user.linkedin_url,
            github_url=user.github_url,
            website_url=user.website_url,
            privacy_settings=user.privacy_settings or {},
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
        
    except Exception as e:
        logger.error("Failed to get user profile", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.put("/profile", response_model=UserProfileResponse)
@limiter.limit("10/minute")
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile
    """
    try:
        user_service = UserService(db)
        
        # Only include non-None values
        update_data = profile_update.model_dump(exclude_unset=True)
        
        user = await user_service.update_user(current_user["user_id"], update_data)
        
        return UserProfileResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            profile_picture_url=user.profile_picture_url,
            bio=user.bio,
            location=user.location,
            linkedin_url=user.linkedin_url,
            github_url=user.github_url,
            website_url=user.website_url,
            privacy_settings=user.privacy_settings or {},
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
        
    except Exception as e:
        logger.error("Failed to update user profile", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.put("/privacy-settings")
@limiter.limit("5/minute")
async def update_privacy_settings(
    privacy_update: PrivacySettingsUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user privacy settings
    """
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(current_user["user_id"])
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Merge with existing privacy settings
        current_settings = user.privacy_settings or {}
        update_data = privacy_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            current_settings[key] = value
        
        updated_user = await user_service.update_user(
            current_user["user_id"], 
            {"privacy_settings": current_settings}
        )
        
        return {"message": "Privacy settings updated successfully", "settings": updated_user.privacy_settings}
        
    except Exception as e:
        logger.error("Failed to update privacy settings", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update privacy settings"
        )


@router.get("/{user_id}/profile", response_model=UserProfileResponse)
async def get_public_user_profile(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get another user's public profile
    """
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check privacy settings
        if not user.privacy_settings.get("profile_visible", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User profile is private"
            )
        
        # Return limited profile info for public view
        return UserProfileResponse(
            id=str(user.id),
            email=user.email,  # This could be hidden based on privacy settings
            full_name=user.full_name,
            profile_picture_url=user.profile_picture_url,
            bio=user.bio,
            location=user.location,
            linkedin_url=user.linkedin_url,
            github_url=user.github_url,
            website_url=user.website_url,
            privacy_settings={},  # Don't expose privacy settings to others
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get public user profile", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.post("/deactivate")
@limiter.limit("2/hour")
async def deactivate_account(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Deactivate current user's account
    """
    try:
        user_service = UserService(db)
        await user_service.deactivate_user(current_user["user_id"])
        
        logger.info("User account deactivated", user_id=current_user["user_id"])
        return {"message": "Account deactivated successfully"}
        
    except Exception as e:
        logger.error("Failed to deactivate account", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate account"
        )