"""
Agent management endpoints
"""

from typing import Dict, Any, List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.services.agent_service import AgentService
from app.core.exceptions import AgentNotFoundError, ValidationError

logger = structlog.get_logger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class AgentCreateRequest(BaseModel):
    """Agent creation request"""
    name: str
    personality_type: Optional[str] = "professional"
    persona_description: Optional[str] = None
    conversation_style: Optional[Dict[str, Any]] = None
    goals: Optional[List[str]] = []
    interests: Optional[List[str]] = []


class AgentUpdateRequest(BaseModel):
    """Agent update request"""
    name: Optional[str] = None
    personality_type: Optional[str] = None
    persona_description: Optional[str] = None
    conversation_style: Optional[Dict[str, Any]] = None
    background_context: Optional[str] = None
    goals: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class AgentResponse(BaseModel):
    """Agent response model"""
    id: str
    user_id: str
    name: str
    personality_type: str
    persona_description: Optional[str] = None
    conversation_style: Dict[str, Any]
    background_context: Optional[str] = None
    goals: List[str]
    interests: List[str]
    is_active: bool
    last_conversation_at: Optional[str] = None
    total_conversations: int
    created_at: str
    updated_at: str


@router.get("/", response_model=List[AgentResponse])
async def get_user_agents(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all agents for the current user
    """
    try:
        agent_service = AgentService(db)
        agents = await agent_service.get_agents_by_user_id(current_user["user_id"])
        
        return [
            AgentResponse(
                id=str(agent.id),
                user_id=str(agent.user_id),
                name=agent.name,
                personality_type=agent.personality_type or "professional",
                persona_description=agent.persona_description,
                conversation_style=agent.conversation_style or {},
                background_context=agent.background_context,
                goals=agent.goals or [],
                interests=agent.interests or [],
                is_active=agent.is_active,
                last_conversation_at=agent.last_conversation_at.isoformat() if agent.last_conversation_at else None,
                total_conversations=agent.total_conversations,
                created_at=agent.created_at.isoformat(),
                updated_at=agent.updated_at.isoformat()
            )
            for agent in agents
        ]
        
    except Exception as e:
        logger.error("Failed to get user agents", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get agents"
        )


@router.post("/", response_model=AgentResponse)
@limiter.limit("5/minute")
async def create_agent(
    agent_request: AgentCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new digital twin agent
    """
    try:
        agent_service = AgentService(db)
        
        agent_data = agent_request.model_dump()
        agent = await agent_service.create_agent(current_user["user_id"], agent_data)
        
        return AgentResponse(
            id=str(agent.id),
            user_id=str(agent.user_id),
            name=agent.name,
            personality_type=agent.personality_type or "professional",
            persona_description=agent.persona_description,
            conversation_style=agent.conversation_style or {},
            background_context=agent.background_context,
            goals=agent.goals or [],
            interests=agent.interests or [],
            is_active=agent.is_active,
            last_conversation_at=agent.last_conversation_at.isoformat() if agent.last_conversation_at else None,
            total_conversations=agent.total_conversations,
            created_at=agent.created_at.isoformat(),
            updated_at=agent.updated_at.isoformat()
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logger.error("Failed to create agent", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create agent"
        )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific agent by ID
    """
    try:
        agent_service = AgentService(db)
        agent = await agent_service.get_agent_by_id(agent_id)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        # Verify ownership
        if str(agent.user_id) != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this agent"
            )
        
        return AgentResponse(
            id=str(agent.id),
            user_id=str(agent.user_id),
            name=agent.name,
            personality_type=agent.personality_type or "professional",
            persona_description=agent.persona_description,
            conversation_style=agent.conversation_style or {},
            background_context=agent.background_context,
            goals=agent.goals or [],
            interests=agent.interests or [],
            is_active=agent.is_active,
            last_conversation_at=agent.last_conversation_at.isoformat() if agent.last_conversation_at else None,
            total_conversations=agent.total_conversations,
            created_at=agent.created_at.isoformat(),
            updated_at=agent.updated_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get agent", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get agent"
        )


@router.put("/{agent_id}", response_model=AgentResponse)
@limiter.limit("10/minute")
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an agent's configuration
    """
    try:
        agent_service = AgentService(db)
        
        update_data = agent_update.model_dump(exclude_unset=True)
        agent = await agent_service.update_agent(agent_id, current_user["user_id"], update_data)
        
        return AgentResponse(
            id=str(agent.id),
            user_id=str(agent.user_id),
            name=agent.name,
            personality_type=agent.personality_type or "professional",
            persona_description=agent.persona_description,
            conversation_style=agent.conversation_style or {},
            background_context=agent.background_context,
            goals=agent.goals or [],
            interests=agent.interests or [],
            is_active=agent.is_active,
            last_conversation_at=agent.last_conversation_at.isoformat() if agent.last_conversation_at else None,
            total_conversations=agent.total_conversations,
            created_at=agent.created_at.isoformat(),
            updated_at=agent.updated_at.isoformat()
        )
        
    except AgentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logger.error("Failed to update agent", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent"
        )


@router.delete("/{agent_id}")
@limiter.limit("5/minute")
async def delete_agent(
    agent_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete (deactivate) an agent
    """
    try:
        agent_service = AgentService(db)
        await agent_service.delete_agent(agent_id, current_user["user_id"])
        
        return {"message": "Agent deleted successfully"}
        
    except AgentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error("Failed to delete agent", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete agent"
        )


@router.post("/{agent_id}/activate")
@limiter.limit("5/minute")
async def activate_agent(
    agent_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Activate an agent
    """
    try:
        agent_service = AgentService(db)
        await agent_service.activate_agent(agent_id, current_user["user_id"])
        
        return {"message": "Agent activated successfully"}
        
    except AgentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error("Failed to activate agent", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate agent"
        )