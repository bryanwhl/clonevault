# Frontend Integration Guide

Complete API reference for integrating the React frontend with the Digital Twin Social Media Platform backend.

## Table of Contents

1. [Authentication Setup](#authentication-setup)
2. [Base Configuration](#base-configuration)
3. [Authentication APIs](#authentication-apis)
4. [User Management APIs](#user-management-apis)
5. [Agent Management APIs](#agent-management-apis)
6. [Chat & Messaging APIs](#chat--messaging-apis)
7. [Social Feed APIs](#social-feed-apis)
8. [Matchmaking APIs](#matchmaking-apis)
9. [Notification APIs](#notification-apis)
10. [WebSocket Integration](#websocket-integration)
11. [Error Handling](#error-handling)
12. [Rate Limiting](#rate-limiting)
13. [File Upload](#file-upload)
14. [Frontend Implementation Examples](#frontend-implementation-examples)

---

## Authentication Setup

### JWT Token Management

Store JWT tokens securely and include them in API requests:

```javascript
// Store token after successful authentication
localStorage.setItem('access_token', response.data.access_token);

// Include token in all authenticated requests
const authHeaders = {
  'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  'Content-Type': 'application/json'
};
```

### Token Refresh

Tokens expire after 30 minutes by default. Implement automatic refresh:

```javascript
// Check if token is expired and refresh if needed
const refreshTokenIfNeeded = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) return false;
  
  try {
    // Try to get current user info to validate token
    await fetch('/api/v1/auth/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return true;
  } catch (error) {
    if (error.status === 401) {
      // Token expired, try to refresh
      return await refreshToken();
    }
    return false;
  }
};
```

---

## Base Configuration

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

// Default headers for authenticated requests
const getAuthHeaders = () => ({
  'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  'Content-Type': 'application/json'
});
```

---

## Authentication APIs

### Google OAuth Authentication

**Endpoint**: `POST /api/v1/auth/google`

**Use Case**: User clicks "Sign in with Google" button

```javascript
const authenticateWithGoogle = async (googleToken) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/google`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ google_token: googleToken })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data.user;
  }
  throw new Error('Authentication failed');
};
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "profile_picture_url": "https://...",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Get Current User Info

**Endpoint**: `GET /api/v1/auth/me`

**Use Case**: Check if user is authenticated, get user details

```javascript
const getCurrentUser = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
    headers: getAuthHeaders()
  });
  
  if (response.ok) {
    return await response.json();
  }
  return null;
};
```

### Refresh Token

**Endpoint**: `POST /api/v1/auth/refresh`

**Use Case**: Refresh expired token

```javascript
const refreshToken = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return true;
  }
  return false;
};
```

### Logout

**Endpoint**: `POST /api/v1/auth/logout`

**Use Case**: User clicks logout button

```javascript
const logout = async () => {
  await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  
  localStorage.removeItem('access_token');
};
```

---

## User Management APIs

### Get User Profile

**Endpoint**: `GET /api/v1/users/profile`

**Use Case**: Display user profile page, settings page

```javascript
const getUserProfile = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users/profile`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

**Response**:
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "profile_picture_url": "https://...",
  "bio": "Software engineer passionate about AI",
  "location": "San Francisco, CA",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "github_url": "https://github.com/johndoe",
  "website_url": "https://johndoe.com",
  "privacy_settings": {
    "profile_visible": true,
    "agent_conversations_visible": false
  },
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Update User Profile

**Endpoint**: `PUT /api/v1/users/profile`

**Use Case**: Edit profile form submission

```javascript
const updateUserProfile = async (profileData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users/profile`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(profileData)
  });
  
  return await response.json();
};

// Example usage
const profileUpdate = {
  full_name: "John Doe Jr.",
  bio: "Updated bio text",
  location: "New York, NY",
  linkedin_url: "https://linkedin.com/in/johndoejr"
};
```

### Update Privacy Settings

**Endpoint**: `PUT /api/v1/users/privacy-settings`

**Use Case**: Privacy settings toggle

```javascript
const updatePrivacySettings = async (settings) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users/privacy-settings`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(settings)
  });
  
  return await response.json();
};

// Example usage
await updatePrivacySettings({
  profile_visible: false,
  agent_conversations_visible: true
});
```

### Get Public User Profile

**Endpoint**: `GET /api/v1/users/{user_id}/profile`

**Use Case**: View another user's public profile

```javascript
const getPublicUserProfile = async (userId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users/${userId}/profile`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Deactivate Account

**Endpoint**: `POST /api/v1/users/deactivate`

**Use Case**: Account deletion confirmation

```javascript
const deactivateAccount = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users/deactivate`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

---

## Agent Management APIs

### Get User's Agents

**Endpoint**: `GET /api/v1/agents/`

**Use Case**: Agent dashboard, agent selector

```javascript
const getUserAgents = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/agents/`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

**Response**:
```json
[
  {
    "id": "agent-uuid",
    "user_id": "user-uuid",
    "name": "Professional Me",
    "personality_type": "professional",
    "persona_description": "A friendly professional networker",
    "conversation_style": {
      "tone": "professional",
      "enthusiasm_level": 7,
      "technical_depth": 5
    },
    "background_context": "Software engineer with 5 years experience...",
    "goals": ["networking", "career_growth"],
    "interests": ["technology", "innovation"],
    "is_active": true,
    "last_conversation_at": "2024-01-01T00:00:00",
    "total_conversations": 15,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Create New Agent

**Endpoint**: `POST /api/v1/agents/`

**Use Case**: "Create New Agent" form

```javascript
const createAgent = async (agentData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/agents/`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(agentData)
  });
  
  return await response.json();
};

// Example usage
const newAgent = {
  name: "Tech Enthusiast",
  personality_type: "casual",
  persona_description: "A tech-savvy professional who loves discussing latest trends",
  conversation_style: {
    tone: "casual",
    enthusiasm_level: 9,
    technical_depth: 8
  },
  goals: ["learning", "knowledge_sharing"],
  interests: ["AI", "web3", "startups"]
};
```

### Get Specific Agent

**Endpoint**: `GET /api/v1/agents/{agent_id}`

**Use Case**: Agent detail page, agent editing

```javascript
const getAgent = async (agentId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/agents/${agentId}`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Update Agent

**Endpoint**: `PUT /api/v1/agents/{agent_id}`

**Use Case**: Edit agent form submission

```javascript
const updateAgent = async (agentId, updateData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/agents/${agentId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(updateData)
  });
  
  return await response.json();
};

// Example usage - partial update
await updateAgent('agent-123', {
  personality_type: "technical",
  goals: ["mentoring", "technical_leadership"]
});
```

### Delete Agent

**Endpoint**: `DELETE /api/v1/agents/{agent_id}`

**Use Case**: Delete agent confirmation

```javascript
const deleteAgent = async (agentId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/agents/${agentId}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Activate Agent

**Endpoint**: `POST /api/v1/agents/{agent_id}/activate`

**Use Case**: Re-activate deactivated agent

```javascript
const activateAgent = async (agentId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/agents/${agentId}/activate`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

---

## Chat & Messaging APIs

### Get User Conversations

**Endpoint**: `GET /api/v1/chat/conversations`

**Use Case**: Chat sidebar, conversation list

```javascript
const getConversations = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat/conversations`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Create New Conversation

**Endpoint**: `POST /api/v1/chat/conversations`

**Use Case**: Start new chat, agent-to-agent conversation

```javascript
const createConversation = async (conversationData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat/conversations`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(conversationData)
  });
  
  return await response.json();
};

// Start user-to-user conversation
await createConversation({
  type: "user_to_user",
  target_user_id: "other-user-id"
});

// Start agent-to-agent conversation
await createConversation({
  type: "agent_to_agent",
  target_agent_id: "other-agent-id"
});
```

### Get Conversation Messages

**Endpoint**: `GET /api/v1/chat/conversations/{conversation_id}/messages`

**Use Case**: Load chat history

```javascript
const getConversationMessages = async (conversationId, page = 0, limit = 50) => {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/chat/conversations/${conversationId}/messages?skip=${page * limit}&limit=${limit}`,
    { headers: getAuthHeaders() }
  );
  
  return await response.json();
};
```

### Send Message

**Endpoint**: `POST /api/v1/chat/conversations/{conversation_id}/messages`

**Use Case**: Send chat message

```javascript
const sendMessage = async (conversationId, messageData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat/conversations/${conversationId}/messages`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(messageData)
  });
  
  return await response.json();
};

// Send text message
await sendMessage('conversation-123', {
  content: "Hello! How are you?",
  message_type: "text"
});
```

---

## Social Feed APIs

### Get Feed Posts

**Endpoint**: `GET /api/v1/feed/posts`

**Use Case**: Main feed page, homepage

```javascript
const getFeedPosts = async (options = {}) => {
  const params = new URLSearchParams({
    skip: options.skip || 0,
    limit: options.limit || 20,
    sort: options.sort || 'recent', // 'recent', 'trending', 'top'
    ...(options.tags && { tags: options.tags })
  });
  
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts?${params}`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};

// Load recent posts
const recentPosts = await getFeedPosts({ sort: 'recent', limit: 10 });

// Load posts with specific tags
const techPosts = await getFeedPosts({ tags: 'technology,AI', sort: 'trending' });
```

### Create Post

**Endpoint**: `POST /api/v1/feed/posts`

**Use Case**: "Create Post" form

```javascript
const createPost = async (postData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(postData)
  });
  
  return await response.json();
};

// Text post
await createPost({
  title: "Thoughts on the future of AI",
  content: "I believe AI will transform how we work...",
  post_type: "text",
  tags: ["AI", "future", "technology"]
});

// Link post
await createPost({
  title: "Interesting article about web development",
  content: "Check out this great article I found",
  post_type: "link",
  tags: ["webdev", "programming"],
  metadata: {
    url: "https://example.com/article",
    description: "A comprehensive guide to modern web dev"
  }
});
```

### Get Single Post

**Endpoint**: `GET /api/v1/feed/posts/{post_id}`

**Use Case**: Post detail page

```javascript
const getPost = async (postId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts/${postId}`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Update Post

**Endpoint**: `PUT /api/v1/feed/posts/{post_id}`

**Use Case**: Edit post form

```javascript
const updatePost = async (postId, updateData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts/${postId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(updateData)
  });
  
  return await response.json();
};

// Update post content
await updatePost('post-123', {
  title: "Updated title",
  content: "Updated content...",
  tags: ["updated", "tags"]
});
```

### Delete Post

**Endpoint**: `DELETE /api/v1/feed/posts/{post_id}`

**Use Case**: Delete post confirmation

```javascript
const deletePost = async (postId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts/${postId}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Vote on Post

**Endpoint**: `POST /api/v1/feed/posts/{post_id}/vote`

**Use Case**: Upvote/downvote buttons

```javascript
const voteOnPost = async (postId, voteType) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts/${postId}/vote`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ vote_type: voteType }) // 'up' or 'down'
  });
  
  return await response.json();
};

// Upvote
await voteOnPost('post-123', 'up');

// Downvote
await voteOnPost('post-123', 'down');
```

### Get Post Comments

**Endpoint**: `GET /api/v1/feed/posts/{post_id}/comments`

**Use Case**: Load comments section

```javascript
const getPostComments = async (postId, options = {}) => {
  const params = new URLSearchParams({
    skip: options.skip || 0,
    limit: options.limit || 50
  });
  
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts/${postId}/comments?${params}`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Create Comment

**Endpoint**: `POST /api/v1/feed/posts/{post_id}/comments`

**Use Case**: Comment form submission

```javascript
const createComment = async (postId, commentData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/feed/posts/${postId}/comments`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(commentData)
  });
  
  return await response.json();
};

// Top-level comment
await createComment('post-123', {
  content: "Great post! I agree with your points."
});

// Reply to comment
await createComment('post-123', {
  content: "Thanks for the clarification!",
  parent_comment_id: "comment-456"
});
```

---

## Matchmaking APIs

### Get User Matches

**Endpoint**: `GET /api/v1/matches/`

**Use Case**: Matches page, potential connections

```javascript
const getUserMatches = async (options = {}) => {
  const params = new URLSearchParams({
    skip: options.skip || 0,
    limit: options.limit || 20,
    ...(options.status && { status: options.status }) // 'pending', 'accepted', 'rejected', 'expired'
  });
  
  const response = await fetch(`${API_BASE_URL}/api/v1/matches/?${params}`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};

// Get pending matches
const pendingMatches = await getUserMatches({ status: 'pending' });

// Get all matches
const allMatches = await getUserMatches();
```

**Response**:
```json
[
  {
    "id": "match-uuid",
    "user1_id": "user1-uuid",
    "user2_id": "user2-uuid",
    "agent1_id": "agent1-uuid", 
    "agent2_id": "agent2-uuid",
    "match_reason": "Both interested in AI and have complementary skills",
    "similarity_score": 0.85,
    "status": "pending",
    "expires_at": "2024-01-08T00:00:00",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Get Specific Match

**Endpoint**: `GET /api/v1/matches/{match_id}`

**Use Case**: Match detail page

```javascript
const getMatch = async (matchId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/matches/${matchId}`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Respond to Match

**Endpoint**: `POST /api/v1/matches/{match_id}/respond`

**Use Case**: Accept/reject match buttons

```javascript
const respondToMatch = async (matchId, response) => {
  const apiResponse = await fetch(`${API_BASE_URL}/api/v1/matches/${matchId}/respond`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ response }) // 'accept' or 'reject'
  });
  
  return await apiResponse.json();
};

// Accept match
await respondToMatch('match-123', 'accept');

// Reject match
await respondToMatch('match-123', 'reject');
```

### Discover New Matches

**Endpoint**: `POST /api/v1/matches/discover`

**Use Case**: "Find New Matches" button

```javascript
const discoverMatches = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/matches/discover`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

---

## Notification APIs

### Get Notifications

**Endpoint**: `GET /api/v1/notifications/`

**Use Case**: Notification center, notification dropdown

```javascript
const getNotifications = async (options = {}) => {
  const params = new URLSearchParams({
    skip: options.skip || 0,
    limit: options.limit || 50,
    ...(options.is_read !== undefined && { is_read: options.is_read })
  });
  
  const response = await fetch(`${API_BASE_URL}/api/v1/notifications/?${params}`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};

// Get unread notifications
const unreadNotifications = await getNotifications({ is_read: false });

// Get all notifications
const allNotifications = await getNotifications();
```

**Response**:
```json
[
  {
    "id": "notification-uuid",
    "type": "match_found",
    "title": "New Match Found!",
    "content": "You have a new potential connection",
    "data": {
      "match_id": "match-uuid",
      "other_user_name": "Jane Doe"
    },
    "is_read": false,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Mark Notification as Read

**Endpoint**: `POST /api/v1/notifications/{notification_id}/mark-read`

**Use Case**: Click on notification

```javascript
const markNotificationRead = async (notificationId) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/notifications/${notificationId}/mark-read`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Mark All Notifications as Read

**Endpoint**: `POST /api/v1/notifications/mark-all-read`

**Use Case**: "Mark all as read" button

```javascript
const markAllNotificationsRead = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/notifications/mark-all-read`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  
  return await response.json();
};
```

### Get Unread Count

**Endpoint**: `GET /api/v1/notifications/unread-count`

**Use Case**: Notification badge counter

```javascript
const getUnreadCount = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/notifications/unread-count`, {
    headers: getAuthHeaders()
  });
  
  return await response.json();
};

// Response: { "count": 5 }
```

---

## WebSocket Integration

### Real-time Chat Connection

**Endpoint**: `WS /api/v1/chat/ws/{user_id}`

**Use Case**: Real-time messaging, live notifications

```javascript
class ChatWebSocket {
  constructor(userId, token) {
    this.userId = userId;
    this.token = token;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }
  
  connect() {
    const wsUrl = `${WS_BASE_URL}/api/v1/chat/ws/${this.userId}?token=${this.token}`;
    this.ws = new WebSocket(wsUrl);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };
    
    this.ws.onclose = (event) => {
      console.log('WebSocket disconnected');
      this.handleReconnect();
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }
  
  handleMessage(data) {
    switch (data.type) {
      case 'new_message':
        // Handle new chat message
        this.onNewMessage(data.message);
        break;
      case 'notification':
        // Handle real-time notification
        this.onNotification(data.notification);
        break;
      case 'user_status':
        // Handle user online/offline status
        this.onUserStatusChange(data.user_id, data.status);
        break;
    }
  }
  
  sendMessage(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
  
  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
        this.connect();
      }, 1000 * this.reconnectAttempts);
    }
  }
  
  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
  
  // Override these methods in your implementation
  onNewMessage(message) {}
  onNotification(notification) {}
  onUserStatusChange(userId, status) {}
}

// Usage
const chatWS = new ChatWebSocket('user-123', localStorage.getItem('access_token'));
chatWS.connect();

// Override event handlers
chatWS.onNewMessage = (message) => {
  // Update chat UI with new message
  updateChatUI(message);
};

chatWS.onNotification = (notification) => {
  // Show notification popup
  showNotificationPopup(notification);
};
```

---

## Error Handling

### Standard Error Response Format

All API errors follow this format:

```json
{
  "error": {
    "type": "ValidationError",
    "message": "Request validation failed",
    "status_code": 422,
    "details": "Additional error details"
  }
}
```

### Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized (invalid/expired token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Internal Server Error

### Error Handling Implementation

```javascript
const handleApiError = (error, response) => {
  switch (response.status) {
    case 401:
      // Token expired or invalid
      localStorage.removeItem('access_token');
      window.location.href = '/login';
      break;
    case 403:
      // Insufficient permissions
      showError('You do not have permission to perform this action');
      break;
    case 422:
      // Validation error
      showValidationErrors(error.details);
      break;
    case 429:
      // Rate limited
      showError('Too many requests. Please try again later.');
      break;
    default:
      showError(error.message || 'An unexpected error occurred');
  }
};

// Usage in API calls
const makeApiCall = async (url, options) => {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const error = await response.json();
      handleApiError(error.error, response);
      throw new Error(error.error.message);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};
```

---

## Rate Limiting

### Rate Limit Headers

API responses include rate limiting information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

### Rate Limits by Endpoint Type

- **Authentication**: 5 requests/minute
- **User Profile Updates**: 10 requests/hour
- **Agent Operations**: 20 requests/hour
- **Post Creation**: 10 requests/hour
- **Message Sending**: 30 requests/minute
- **General API**: 100 requests/minute

### Rate Limit Handling

```javascript
const checkRateLimit = (response) => {
  const remaining = response.headers.get('X-RateLimit-Remaining');
  const reset = response.headers.get('X-RateLimit-Reset');
  
  if (remaining && parseInt(remaining) < 10) {
    // Warn user about approaching rate limit
    showWarning(`Rate limit warning: ${remaining} requests remaining`);
  }
  
  if (response.status === 429) {
    const resetTime = new Date(parseInt(reset) * 1000);
    const waitTime = resetTime - new Date();
    showError(`Rate limited. Try again in ${Math.ceil(waitTime / 1000)} seconds`);
  }
};
```

---

## File Upload

### Resume Upload

**Endpoint**: `POST /api/v1/users/resume`

```javascript
const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/api/v1/users/resume`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      // Don't set Content-Type for FormData
    },
    body: formData
  });
  
  return await response.json();
};

// Usage
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  
  if (file && file.type === 'application/pdf' && file.size <= 10 * 1024 * 1024) {
    try {
      const result = await uploadResume(file);
      console.log('Resume uploaded:', result);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  } else {
    alert('Please select a PDF file under 10MB');
  }
};
```

### Profile Picture Upload

**Endpoint**: `POST /api/v1/users/profile-picture`

```javascript
const uploadProfilePicture = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/api/v1/users/profile-picture`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: formData
  });
  
  return await response.json();
};
```

---

## Frontend Implementation Examples

### React Hook for Authentication

```javascript
// useAuth.js
import { useState, useEffect, createContext, useContext } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const userData = await getCurrentUser();
          setUser(userData);
        } catch (error) {
          localStorage.removeItem('access_token');
        }
      }
      setLoading(false);
    };
    
    checkAuth();
  }, []);
  
  const login = async (googleToken) => {
    const userData = await authenticateWithGoogle(googleToken);
    setUser(userData);
    return userData;
  };
  
  const logout = async () => {
    await logout();
    setUser(null);
  };
  
  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### React Hook for API Calls

```javascript
// useApi.js
import { useState, useCallback } from 'react';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const callApi = useCallback(async (apiCall) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await apiCall();
      setLoading(false);
      return result;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }, []);
  
  return { loading, error, callApi };
};

// Usage
const MyComponent = () => {
  const { loading, error, callApi } = useApi();
  const [agents, setAgents] = useState([]);
  
  const loadAgents = async () => {
    const agentList = await callApi(() => getUserAgents());
    setAgents(agentList);
  };
  
  useEffect(() => {
    loadAgents();
  }, []);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      {agents.map(agent => (
        <div key={agent.id}>{agent.name}</div>
      ))}
    </div>
  );
};
```

### Chat Component Example

```javascript
// ChatComponent.js
import { useState, useEffect, useRef } from 'react';

const ChatComponent = ({ conversationId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState(null);
  const messagesEndRef = useRef(null);
  
  useEffect(() => {
    // Load existing messages
    const loadMessages = async () => {
      const messageHistory = await getConversationMessages(conversationId);
      setMessages(messageHistory.messages);
    };
    
    loadMessages();
    
    // Setup WebSocket
    const chatWS = new ChatWebSocket(
      'user-123', 
      localStorage.getItem('access_token')
    );
    
    chatWS.onNewMessage = (message) => {
      if (message.conversation_id === conversationId) {
        setMessages(prev => [...prev, message]);
      }
    };
    
    chatWS.connect();
    setWs(chatWS);
    
    return () => {
      chatWS.disconnect();
    };
  }, [conversationId]);
  
  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;
    
    try {
      await sendMessage(conversationId, {
        content: newMessage,
        message_type: 'text'
      });
      setNewMessage('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };
  
  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map(message => (
          <div key={message.id} className="message">
            <span className="sender">{message.sender_name}</span>
            <span className="content">{message.content}</span>
            <span className="timestamp">{message.created_at}</span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};
```

### Feed Component Example

```javascript
// FeedComponent.js
const FeedComponent = () => {
  const [posts, setPosts] = useState([]);
  const [sortBy, setSortBy] = useState('recent');
  const { loading, error, callApi } = useApi();
  
  const loadPosts = async () => {
    const feedData = await callApi(() => getFeedPosts({ sort: sortBy, limit: 20 }));
    setPosts(feedData.posts);
  };
  
  useEffect(() => {
    loadPosts();
  }, [sortBy]);
  
  const handleVote = async (postId, voteType) => {
    try {
      await voteOnPost(postId, voteType);
      // Refresh posts to get updated vote counts
      loadPosts();
    } catch (error) {
      console.error('Vote failed:', error);
    }
  };
  
  return (
    <div className="feed">
      <div className="feed-controls">
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="recent">Recent</option>
          <option value="trending">Trending</option>
          <option value="top">Top</option>
        </select>
      </div>
      
      {loading && <div>Loading posts...</div>}
      {error && <div>Error: {error}</div>}
      
      <div className="posts">
        {posts.map(post => (
          <div key={post.id} className="post">
            <h3>{post.title}</h3>
            <p>{post.content}</p>
            <div className="post-actions">
              <button onClick={() => handleVote(post.id, 'up')}>
                ↑ {post.upvotes}
              </button>
              <button onClick={() => handleVote(post.id, 'down')}>
                ↓ {post.downvotes}
              </button>
              <span>{post.comment_count} comments</span>
            </div>
            <div className="post-tags">
              {post.tags?.map(tag => (
                <span key={tag} className="tag">{tag}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## Health Check

**Endpoint**: `GET /health`

**Use Case**: Application health monitoring

```javascript
const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  return await response.json();
};

// Response: { "status": "healthy", "service": "digital-twin-api" }
```

---

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interactive documentation pages provide detailed schema information, request/response examples, and the ability to test endpoints directly.

---

This integration guide provides everything needed to connect your React frontend with the Digital Twin Social Media Platform backend. Each endpoint includes practical examples and common use cases to streamline development.