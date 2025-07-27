"""
Agent service for managing digital twin agents
"""

from typing import Dict, Any, Optional, List
import uuid

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.agent import Agent
from app.models.user import User
from app.core.exceptions import AgentNotFoundError, UserNotFoundError, ValidationError

logger = structlog.get_logger(__name__)


class AgentService:
    """Service for agent-related operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        try:
            agent_uuid = uuid.UUID(agent_id)
            stmt = select(Agent).where(Agent.id == agent_uuid)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except ValueError:
            raise ValidationError("Invalid agent ID format")
    
    async def get_agents_by_user_id(self, user_id: str) -> List[Agent]:
        """Get all agents for a user"""
        try:
            user_uuid = uuid.UUID(user_id)
            stmt = select(Agent).where(Agent.user_id == user_uuid).where(Agent.is_active == True)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except ValueError:
            raise ValidationError("Invalid user ID format")
    
    async def create_agent(self, user_id: str, agent_data: Dict[str, Any]) -> Agent:
        """Create a new agent for a user"""
        try:
            user_uuid = uuid.UUID(user_id)
            
            # Verify user exists
            user_stmt = select(User).where(User.id == user_uuid)
            user_result = await self.db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise UserNotFoundError(user_id)
            
            agent = Agent(
                user_id=user_uuid,
                name=agent_data["name"],
                personality_type=agent_data.get("personality_type", "professional"),
                persona_description=agent_data.get("persona_description"),
                conversation_style=agent_data.get("conversation_style", {
                    "tone": "professional",
                    "enthusiasm_level": 7,
                    "technical_depth": 5
                }),
                background_context=agent_data.get("background_context"),
                goals=agent_data.get("goals", []),
                interests=agent_data.get("interests", [])
            )
            
            self.db.add(agent)
            await self.db.commit()
            await self.db.refresh(agent)
            
            logger.info("Agent created successfully", agent_id=str(agent.id), user_id=user_id)
            return agent
            
        except ValueError:
            raise ValidationError("Invalid user ID format")
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("Failed to create agent", error=str(e))
            raise ValidationError("Failed to create agent")
    
    async def update_agent(self, agent_id: str, user_id: str, agent_data: Dict[str, Any]) -> Agent:
        """Update agent information"""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise AgentNotFoundError(agent_id)
        
        # Verify ownership
        if str(agent.user_id) != user_id:
            raise ValidationError("You don't have permission to update this agent")
        
        # Update allowed fields
        allowed_fields = [
            "name", "personality_type", "persona_description", 
            "conversation_style", "background_context", "goals", "interests"
        ]
        
        for field in allowed_fields:
            if field in agent_data:
                setattr(agent, field, agent_data[field])
        
        try:
            await self.db.commit()
            await self.db.refresh(agent)
            
            logger.info("Agent updated successfully", agent_id=agent_id)
            return agent
            
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("Failed to update agent", error=str(e))
            raise ValidationError("Failed to update agent")
    
    async def delete_agent(self, agent_id: str, user_id: str) -> bool:
        """Delete (deactivate) an agent"""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise AgentNotFoundError(agent_id)
        
        # Verify ownership
        if str(agent.user_id) != user_id:
            raise ValidationError("You don't have permission to delete this agent")
        
        agent.is_active = False
        await self.db.commit()
        
        logger.info("Agent deactivated", agent_id=agent_id, user_id=user_id)
        return True
    
    async def activate_agent(self, agent_id: str, user_id: str) -> bool:
        """Activate an agent"""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise AgentNotFoundError(agent_id)
        
        # Verify ownership
        if str(agent.user_id) != user_id:
            raise ValidationError("You don't have permission to activate this agent")
        
        agent.is_active = True
        await self.db.commit()
        
        logger.info("Agent activated", agent_id=agent_id, user_id=user_id)
        return True
    
    async def update_agent_context_from_resume(self, agent_id: str, resume_data: Dict[str, Any]) -> Agent:
        """Update agent's background context from parsed resume data"""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise AgentNotFoundError(agent_id)
        
        # Build background context from resume
        context_parts = []
        
        personal_info = resume_data.get("personal_info", {})
        experience = resume_data.get("experience", [])
        education = resume_data.get("education", [])
        skills = resume_data.get("skills", [])
        projects = resume_data.get("projects", [])
        
        if personal_info.get("name"):
            context_parts.append(f"Name: {personal_info['name']}")
        
        if experience:
            exp_summary = "Professional Experience:\n"
            for exp in experience[:3]:  # Top 3 experiences
                title = exp.get("title", "Unknown role")
                exp_summary += f"- {title}\n"
            context_parts.append(exp_summary)
        
        if education:
            edu_summary = "Education:\n"
            for edu in education:
                institution = edu.get("institution", "Educational institution")
                edu_summary += f"- {institution}\n"
            context_parts.append(edu_summary)
        
        if skills:
            skills_summary = f"Skills: {', '.join(skills[:10])}"  # Top 10 skills
            context_parts.append(skills_summary)
        
        if projects:
            proj_summary = "Projects:\n"
            for proj in projects[:3]:  # Top 3 projects
                name = proj.get("name", "Project")
                proj_summary += f"- {name}\n"
            context_parts.append(proj_summary)
        
        background_context = "\n\n".join(context_parts)
        
        # Update agent
        agent.background_context = background_context
        await self.db.commit()
        await self.db.refresh(agent)
        
        logger.info("Agent context updated from resume", agent_id=agent_id)
        return agent
    
    async def increment_conversation_count(self, agent_id: str) -> None:
        """Increment the conversation count for an agent"""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise AgentNotFoundError(agent_id)
        
        agent.total_conversations += 1
        from datetime import datetime
        agent.last_conversation_at = datetime.utcnow()
        await self.db.commit()
        
        logger.debug("Agent conversation count incremented", agent_id=agent_id)