"""
Tests for agent endpoints
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAgentEndpoints:
    """Test agent management endpoints"""
    
    @patch('app.core.security.get_current_active_user')
    @patch('app.services.agent_service.AgentService.get_agents_by_user_id')
    def test_get_user_agents(self, mock_get_agents, mock_get_user, client):
        """Test getting user's agents"""
        # Mock authenticated user
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        # Mock agents
        mock_agent = MagicMock()
        mock_agent.id = "agent-123"
        mock_agent.user_id = "user-123"
        mock_agent.name = "Test Agent"
        mock_agent.personality_type = "professional"
        mock_agent.persona_description = "A test agent"
        mock_agent.conversation_style = {"tone": "friendly"}
        mock_agent.background_context = "Test background"
        mock_agent.goals = ["networking"]
        mock_agent.interests = ["technology"]
        mock_agent.is_active = True
        mock_agent.last_conversation_at = None
        mock_agent.total_conversations = 0
        mock_agent.created_at.isoformat.return_value = "2024-01-01T00:00:00"
        mock_agent.updated_at.isoformat.return_value = "2024-01-01T00:00:00"
        
        mock_get_agents.return_value = [mock_agent]
        
        response = client.get("/api/v1/agents/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Agent"
        assert data[0]["personality_type"] == "professional"
    
    @patch('app.core.security.get_current_active_user')
    @patch('app.services.agent_service.AgentService.create_agent')
    def test_create_agent(self, mock_create_agent, mock_get_user, client, sample_agent_data):
        """Test creating a new agent"""
        # Mock authenticated user
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        # Mock created agent
        mock_agent = MagicMock()
        mock_agent.id = "agent-123"
        mock_agent.user_id = "user-123"
        mock_agent.name = sample_agent_data["name"]
        mock_agent.personality_type = sample_agent_data["personality_type"]
        mock_agent.persona_description = sample_agent_data["persona_description"]
        mock_agent.conversation_style = {}
        mock_agent.background_context = None
        mock_agent.goals = sample_agent_data["goals"]
        mock_agent.interests = sample_agent_data["interests"]
        mock_agent.is_active = True
        mock_agent.last_conversation_at = None
        mock_agent.total_conversations = 0
        mock_agent.created_at.isoformat.return_value = "2024-01-01T00:00:00"
        mock_agent.updated_at.isoformat.return_value = "2024-01-01T00:00:00"
        
        mock_create_agent.return_value = mock_agent
        
        response = client.post("/api/v1/agents/", json=sample_agent_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_agent_data["name"]
        assert data["personality_type"] == sample_agent_data["personality_type"]
    
    @patch('app.core.security.get_current_active_user')
    @patch('app.services.agent_service.AgentService.get_agent_by_id')
    def test_get_agent_by_id(self, mock_get_agent, mock_get_user, client):
        """Test getting a specific agent"""
        # Mock authenticated user
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        # Mock agent
        mock_agent = MagicMock()
        mock_agent.id = "agent-123"
        mock_agent.user_id = "user-123"
        mock_agent.name = "Test Agent"
        mock_agent.personality_type = "professional"
        mock_agent.persona_description = "A test agent"
        mock_agent.conversation_style = {"tone": "friendly"}
        mock_agent.background_context = "Test background"
        mock_agent.goals = ["networking"]
        mock_agent.interests = ["technology"]
        mock_agent.is_active = True
        mock_agent.last_conversation_at = None
        mock_agent.total_conversations = 0
        mock_agent.created_at.isoformat.return_value = "2024-01-01T00:00:00"
        mock_agent.updated_at.isoformat.return_value = "2024-01-01T00:00:00"
        
        mock_get_agent.return_value = mock_agent
        
        response = client.get("/api/v1/agents/agent-123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "agent-123"
        assert data["name"] == "Test Agent"
    
    @patch('app.core.security.get_current_active_user')
    @patch('app.services.agent_service.AgentService.get_agent_by_id')
    def test_get_agent_not_found(self, mock_get_agent, mock_get_user, client):
        """Test getting a non-existent agent"""
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com", 
            "name": "Test User"
        }
        
        mock_get_agent.return_value = None
        
        response = client.get("/api/v1/agents/nonexistent")
        
        assert response.status_code == 404
    
    @patch('app.core.security.get_current_active_user')
    @patch('app.services.agent_service.AgentService.get_agent_by_id')
    def test_get_agent_unauthorized(self, mock_get_agent, mock_get_user, client):
        """Test accessing another user's agent"""
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        # Mock agent belonging to different user
        mock_agent = MagicMock()
        mock_agent.user_id = "other-user-456"
        mock_get_agent.return_value = mock_agent
        
        response = client.get("/api/v1/agents/agent-123")
        
        assert response.status_code == 403
    
    @patch('app.core.security.get_current_active_user')
    @patch('app.services.agent_service.AgentService.delete_agent')
    def test_delete_agent(self, mock_delete_agent, mock_get_user, client):
        """Test deleting an agent"""
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        mock_delete_agent.return_value = True
        
        response = client.delete("/api/v1/agents/agent-123")
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    
    def test_create_agent_unauthenticated(self, client, sample_agent_data):
        """Test creating agent without authentication"""
        response = client.post("/api/v1/agents/", json=sample_agent_data)
        
        assert response.status_code == 403
    
    def test_create_agent_invalid_data(self, client):
        """Test creating agent with invalid data"""
        with patch('app.core.security.get_current_active_user') as mock_get_user:
            mock_get_user.return_value = {
                "user_id": "user-123",
                "email": "test@example.com",
                "name": "Test User"
            }
            
            response = client.post("/api/v1/agents/", json={})
            
            assert response.status_code == 422  # Validation error