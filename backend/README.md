# Digital Twin Social Media Platform - Backend

A production-ready FastAPI backend service for AI-powered agent networking and social interactions.

## Features

- **User Authentication**: JWT-based authentication with Google OAuth
- **Digital Twin Agents**: AI-powered agent configuration and management
- **Real-time Chat**: WebSocket-based messaging system
- **Social Feed**: Posts, comments, and voting system
- **Matchmaking**: Agent-driven user matching with compatibility scoring
- **Vector Search**: Pinecone integration for similarity search
- **Background Tasks**: Celery-based async task processing
- **Comprehensive API**: RESTful endpoints with automatic documentation

## Technology Stack

- **Framework**: FastAPI with async/await patterns
- **Database**: Supabase (PostgreSQL with pgvector extension)
- **Authentication**: JWT with Google OAuth
- **Caching/Queue**: Redis for caching and Celery message broker
- **Vector Database**: Pinecone for similarity searches
- **LLM Integration**: OpenAI API (easily swappable)
- **WebSockets**: Real-time communication
- **Background Tasks**: Celery with Redis broker

## Quick Start

### Prerequisites

- Python 3.13.3+
- Docker and Docker Compose
- Supabase account
- Google OAuth credentials
- OpenAI API key
- Pinecone account

### 1. Clone and Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your actual configuration values
```

### 2. Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

The API will be available at `http://localhost:8000`

### 3. Manual Setup (Alternative)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (required)
redis-server

# Start PostgreSQL with pgvector extension
# Or use the provided docker-compose.yml for just the database

# Run database migrations
python -c "from app.core.database import Base, database_manager; import asyncio; asyncio.run(database_manager.connect())"

# Start the API server
uvicorn main:app --reload

# In separate terminals, start Celery workers
celery -A app.core.celery_app:celery_app worker --loglevel=info
celery -A app.core.celery_app:celery_app beat --loglevel=info

# Optional: Start Flower for task monitoring
celery -A app.core.celery_app:celery_app flower
```

## Configuration

### Environment Variables

Key environment variables you need to set:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Authentication
SECRET_KEY=your-super-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# External Services
OPENAI_API_KEY=sk-your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment

# Redis
REDIS_URL=redis://localhost:6379
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

```
POST /api/v1/auth/google          # Google OAuth authentication
GET  /api/v1/users/profile        # Get user profile
POST /api/v1/agents/              # Create digital twin agent
GET  /api/v1/feed/posts          # Get social feed
POST /api/v1/chat/conversations  # Start conversation
GET  /api/v1/matches/            # Get user matches
```

## Database Schema

The database includes tables for:

- Users and authentication
- Digital twin agents
- Conversations and messages
- Posts, comments, and votes
- Matches and notifications
- Vector embeddings
- Background job tracking

Run the SQL schema file to set up your database:

```bash
psql -d your_database -f database_schema.sql
```

## Background Tasks

The system uses Celery for background processing:

### Task Types

- **Agent Tasks**: Agent conversation processing, persona generation
- **Matchmaking Tasks**: Compatibility scoring, match discovery
- **Notification Tasks**: Real-time notifications, bulk messaging
- **Vector Tasks**: Embedding generation, similarity calculations

### Monitoring

Access the Flower dashboard at `http://localhost:5555` to monitor background tasks.

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/    # API endpoint handlers
│   ├── core/               # Core configuration and utilities
│   ├── models/             # SQLAlchemy database models
│   ├── services/           # Business logic services
│   ├── tasks/              # Celery background tasks
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
└── docker-compose.yml      # Container orchestration
```

### Code Quality

The project follows these standards:

- Type hints throughout the codebase
- Structured logging with context
- Comprehensive error handling
- Input validation and sanitization
- Async/await patterns for I/O operations
- Modular, scalable architecture

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## Deployment

### Production Considerations

1. **Security**: 
   - Use strong secret keys
   - Enable HTTPS
   - Implement rate limiting
   - Secure API keys in environment variables

2. **Performance**:
   - Use Redis for caching
   - Optimize database queries
   - Scale Celery workers based on load
   - Implement connection pooling

3. **Monitoring**:
   - Set up logging aggregation
   - Monitor API response times
   - Track background task completion
   - Monitor database performance

### Container Deployment

The application is containerized and ready for deployment to:

- **Docker Swarm**
- **Kubernetes**
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Heroku**

## Integration with Frontend

This backend is designed to work with the React frontend in `/web_app`. Key integration points:

- **Authentication**: JWT tokens for API access
- **WebSockets**: Real-time chat and notifications
- **File Uploads**: Resume and image handling
- **CORS**: Configured for frontend domains

## Contributing

1. Follow the existing code style and patterns
2. Add tests for new functionality
3. Update documentation as needed
4. Use structured logging for debugging
5. Implement proper error handling

## License

This project is part of the Digital Twin Social Media Platform and follows the same licensing terms as the main project.

## Support

For issues and questions:

1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Monitor background tasks in Flower
4. Check database connectivity and migrations

## API Rate Limits

- Authentication: 5 requests/minute
- User operations: 10-100 requests/hour (varies by endpoint)
- Background task triggers: 5 requests/hour
- General API: 100 requests/minute per user