"""
Custom exceptions and exception handlers
"""

import structlog
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

logger = structlog.get_logger(__name__)


class BaseAPIException(Exception):
    """Base exception for API errors"""
    
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserNotFoundError(BaseAPIException):
    """User not found exception"""
    
    def __init__(self, user_id: str):
        super().__init__(f"User with ID {user_id} not found", status.HTTP_404_NOT_FOUND)


class AgentNotFoundError(BaseAPIException):
    """Agent not found exception"""
    
    def __init__(self, agent_id: str):
        super().__init__(f"Agent with ID {agent_id} not found", status.HTTP_404_NOT_FOUND)


class ConversationNotFoundError(BaseAPIException):
    """Conversation not found exception"""
    
    def __init__(self, conversation_id: str):
        super().__init__(f"Conversation with ID {conversation_id} not found", status.HTTP_404_NOT_FOUND)


class PostNotFoundError(BaseAPIException):
    """Post not found exception"""
    
    def __init__(self, post_id: str):
        super().__init__(f"Post with ID {post_id} not found", status.HTTP_404_NOT_FOUND)


class MatchNotFoundError(BaseAPIException):
    """Match not found exception"""
    
    def __init__(self, match_id: str):
        super().__init__(f"Match with ID {match_id} not found", status.HTTP_404_NOT_FOUND)


class UnauthorizedError(BaseAPIException):
    """Unauthorized access exception"""
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(BaseAPIException):
    """Forbidden access exception"""
    
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ValidationError(BaseAPIException):
    """Validation error exception"""
    
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class FileUploadError(BaseAPIException):
    """File upload error exception"""
    
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ExternalServiceError(BaseAPIException):
    """External service error exception"""
    
    def __init__(self, service_name: str, message: str = None):
        error_message = f"Error communicating with {service_name}"
        if message:
            error_message += f": {message}"
        super().__init__(error_message, status.HTTP_503_SERVICE_UNAVAILABLE)


async def base_exception_handler(request: Request, exc: BaseAPIException) -> JSONResponse:
    """Handler for base API exceptions"""
    logger.error(
        "API Exception",
        path=request.url.path,
        method=request.method,
        status_code=exc.status_code,
        message=exc.message,
        exc_info=exc
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "status_code": exc.status_code
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for general exceptions"""
    logger.error(
        "Unhandled Exception",
        path=request.url.path,
        method=request.method,
        exc_info=exc
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "An internal server error occurred",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        }
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for validation exceptions"""
    logger.warning(
        "Validation Error",
        path=request.url.path,
        method=request.method,
        error=str(exc)
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "type": "ValidationError",
                "message": "Request validation failed",
                "details": str(exc),
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
            }
        }
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup exception handlers for the FastAPI app"""
    
    # Custom exception handlers
    app.add_exception_handler(BaseAPIException, base_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # You can add more specific handlers here
    from fastapi.exceptions import RequestValidationError
    app.add_exception_handler(RequestValidationError, validation_exception_handler)