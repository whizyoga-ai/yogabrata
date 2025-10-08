"""
Custom exceptions for Startup Formation Service
"""

from typing import Any, Dict, Optional


class ServiceError(Exception):
    """Base exception for service errors"""

    def __init__(
        self,
        error_code: str,
        detail: str,
        status_code: int = 500,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.detail = detail
        self.status_code = status_code
        self.metadata = metadata or {}
        super().__init__(detail)


class ValidationError(ServiceError):
    """Raised when input validation fails"""

    def __init__(self, detail: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="VALIDATION_ERROR",
            detail=detail,
            status_code=400,
            metadata=metadata
        )


class WorkflowNotFoundError(ServiceError):
    """Raised when a workflow is not found"""

    def __init__(self, workflow_id: str):
        super().__init__(
            error_code="WORKFLOW_NOT_FOUND",
            detail=f"Workflow with ID '{workflow_id}' not found",
            status_code=404,
            metadata={"workflow_id": workflow_id}
        )


class WorkflowStepError(ServiceError):
    """Raised when a workflow step fails"""

    def __init__(
        self,
        workflow_id: str,
        step_id: str,
        detail: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        metadata = metadata or {}
        metadata.update({"workflow_id": workflow_id, "step_id": step_id})
        super().__init__(
            error_code="WORKFLOW_STEP_ERROR",
            detail=detail,
            status_code=500,
            metadata=metadata
        )


class DocumentGenerationError(ServiceError):
    """Raised when document generation fails"""

    def __init__(
        self,
        document_type: str,
        detail: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        metadata = metadata or {}
        metadata.update({"document_type": document_type})
        super().__init__(
            error_code="DOCUMENT_GENERATION_ERROR",
            detail=detail,
            status_code=500,
            metadata=metadata
        )


class IntegrationError(ServiceError):
    """Raised when external API integration fails"""

    def __init__(
        self,
        integration_name: str,
        detail: str,
        status_code: int = 502,
        metadata: Optional[Dict[str, Any]] = None
    ):
        metadata = metadata or {}
        metadata.update({"integration_name": integration_name})
        super().__init__(
            error_code="INTEGRATION_ERROR",
            detail=detail,
            status_code=status_code,
            metadata=metadata
        )


class DatabaseError(ServiceError):
    """Raised when database operations fail"""

    def __init__(self, detail: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="DATABASE_ERROR",
            detail=detail,
            status_code=500,
            metadata=metadata
        )


class AuthenticationError(ServiceError):
    """Raised when authentication fails"""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            error_code="AUTHENTICATION_ERROR",
            detail=detail,
            status_code=401
        )


class AuthorizationError(ServiceError):
    """Raised when authorization fails"""

    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            error_code="AUTHORIZATION_ERROR",
            detail=detail,
            status_code=403
        )


class RateLimitError(ServiceError):
    """Raised when rate limit is exceeded"""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            error_code="RATE_LIMIT_ERROR",
            detail=detail,
            status_code=429
        )


class ConfigurationError(ServiceError):
    """Raised when there's a configuration error"""

    def __init__(self, detail: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_code="CONFIGURATION_ERROR",
            detail=detail,
            status_code=500,
            metadata=metadata
        )


# Exception handler utilities

def handle_database_errors(func):
    """Decorator to handle database errors"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise DatabaseError(
                detail=f"Database operation failed: {str(e)}",
                metadata={"original_error": str(e)}
            )
    return wrapper


def handle_integration_errors(integration_name: str):
    """Decorator to handle integration errors"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ServiceError:
                raise  # Re-raise service errors
            except Exception as e:
                raise IntegrationError(
                    integration_name=integration_name,
                    detail=f"Integration '{integration_name}' failed: {str(e)}",
                    metadata={"original_error": str(e)}
                )
        return wrapper
    return decorator
