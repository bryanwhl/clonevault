"""
Tests for authentication endpoints
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Digital Twin Social Media Platform API" in response.json()["message"]
    
    @patch('app.core.security.verify_google_token')
    @patch('app.services.user_service.UserService.get_or_create_user_from_google')
    def test_google_auth_success(self, mock_get_user, mock_verify_token, client, sample_user_data):
        """Test successful Google authentication"""
        # Mock the Google token verification
        mock_verify_token.return_value = {
            "google_id": "123456789",
            "email": "test@example.com", 
            "name": "Test User",
            "picture": "https://example.com/avatar.jpg"
        }
        
        # Mock user creation/retrieval
        mock_user = MagicMock()
        mock_user.id = "user-123"
        mock_user.email = "test@example.com"
        mock_user.full_name = "Test User"
        mock_user.profile_picture_url = "https://example.com/avatar.jpg"
        mock_user.created_at.isoformat.return_value = "2024-01-01T00:00:00"
        
        mock_get_user.return_value = mock_user
        
        # Test the endpoint
        response = client.post("/api/v1/auth/google", json={
            "google_token": "fake-google-token"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
    
    def test_google_auth_invalid_token(self, client):
        """Test Google authentication with invalid token"""
        with patch('app.core.security.verify_google_token') as mock_verify:
            mock_verify.side_effect = Exception("Invalid token")
            
            response = client.post("/api/v1/auth/google", json={
                "google_token": "invalid-token"
            })
            
            assert response.status_code == 401
    
    def test_google_auth_missing_token(self, client):
        """Test Google authentication with missing token"""
        response = client.post("/api/v1/auth/google", json={})
        
        assert response.status_code == 422  # Validation error
    
    @patch('app.core.security.get_current_active_user')
    def test_get_current_user_info(self, mock_get_user, client):
        """Test getting current user info"""
        # Mock authenticated user
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        # Mock user service
        with patch('app.services.user_service.UserService.get_user_by_id') as mock_get_by_id:
            mock_user = MagicMock()
            mock_user.id = "user-123"
            mock_user.email = "test@example.com"
            mock_user.full_name = "Test User"
            mock_user.profile_picture_url = None
            mock_user.created_at.isoformat.return_value = "2024-01-01T00:00:00"
            
            mock_get_by_id.return_value = mock_user
            
            response = client.get("/api/v1/auth/me")
            
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "test@example.com"
            assert data["full_name"] == "Test User"
    
    def test_get_current_user_info_unauthenticated(self, client):
        """Test getting user info without authentication"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 403  # No auth header
    
    @patch('app.core.security.get_current_active_user')
    def test_logout(self, mock_get_user, client):
        """Test user logout"""
        mock_get_user.return_value = {
            "user_id": "user-123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        response = client.post("/api/v1/auth/logout")
        
        assert response.status_code == 200
        assert "logged out" in response.json()["message"]