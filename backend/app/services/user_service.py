"""
User service for managing user operations
"""

from typing import Dict, Any, Optional
import uuid

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.exceptions import UserNotFoundError, ValidationError

logger = structlog.get_logger(__name__)


class UserService:
    """Service for user-related operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            user_uuid = uuid.UUID(user_id)
            stmt = select(User).where(User.id == user_uuid)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except ValueError:
            raise ValidationError("Invalid user ID format")
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        """Get user by Google ID"""
        stmt = select(User).where(User.google_id == google_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        try:
            user = User(
                email=user_data["email"],
                google_id=user_data["google_id"],
                full_name=user_data["full_name"],
                profile_picture_url=user_data.get("profile_picture_url"),
                bio=user_data.get("bio"),
                location=user_data.get("location"),
                linkedin_url=user_data.get("linkedin_url"),
                github_url=user_data.get("github_url"),
                website_url=user_data.get("website_url"),
                privacy_settings=user_data.get("privacy_settings", {
                    "profile_visible": True,
                    "agent_conversations_visible": False
                })
            )
            
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info("User created successfully", user_id=str(user.id), email=user.email)
            return user
            
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("Failed to create user", error=str(e))
            raise ValidationError("User with this email or Google ID already exists")
    
    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> User:
        """Update user information"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        
        # Update allowed fields
        allowed_fields = [
            "full_name", "bio", "location", "linkedin_url", 
            "github_url", "website_url", "privacy_settings"
        ]
        
        for field in allowed_fields:
            if field in user_data:
                setattr(user, field, user_data[field])
        
        try:
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info("User updated successfully", user_id=str(user.id))
            return user
            
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("Failed to update user", error=str(e))
            raise ValidationError("Failed to update user")
    
    async def get_or_create_user_from_google(self, google_user_info: Dict[str, Any]) -> User:
        """Get existing user or create new user from Google OAuth info"""
        # First try to find by Google ID
        user = await self.get_user_by_google_id(google_user_info["google_id"])
        
        if user:
            # Update user info if needed
            update_data = {}
            if user.full_name != google_user_info["name"]:
                update_data["full_name"] = google_user_info["name"]
            if user.profile_picture_url != google_user_info.get("picture"):
                update_data["profile_picture_url"] = google_user_info.get("picture")
            
            if update_data:
                user = await self.update_user(str(user.id), update_data)
            
            return user
        
        # Try to find by email
        user = await self.get_user_by_email(google_user_info["email"])
        if user:
            # Update Google ID for existing user
            user.google_id = google_user_info["google_id"]
            await self.db.commit()
            await self.db.refresh(user)
            return user
        
        # Create new user
        user_data = {
            "email": google_user_info["email"],
            "google_id": google_user_info["google_id"],
            "full_name": google_user_info["name"],
            "profile_picture_url": google_user_info.get("picture")
        }
        
        return await self.create_user(user_data)
    
    async def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        
        user.is_active = False
        await self.db.commit()
        
        logger.info("User deactivated", user_id=user_id)
        return True
    
    async def activate_user(self, user_id: str) -> bool:
        """Activate user account"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        
        user.is_active = True
        await self.db.commit()
        
        logger.info("User activated", user_id=user_id)
        return True