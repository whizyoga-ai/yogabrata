"""
Logging configuration for Startup Formation Service
"""

import logging
import sys
from typing import Dict, Any
import structlog
from pythonjsonlogger import jsonlogger

from .config import settings


def setup_logging() -> None:
    """Configure structured logging for the application"""

    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        stream=sys.stdout,
        format="%(message)s",
    )

    # Configure structlog
    if settings.LOG_FORMAT == "json":
        # JSON logging for production
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, settings.LOG_LEVEL.upper())
            ),
            context_class=dict,
            logger_factory=structlog.WriteLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Human-readable logging for development
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, settings.LOG_LEVEL.upper())
            ),
            context_class=dict,
            logger_factory=structlog.WriteLoggerFactory(),
            cache_logger_on_first_use=True,
        )


def get_logger(name: str = None) -> structlog.BoundLoggerBase:
    """Get a structured logger instance"""
    return structlog.get_logger(name or "startup_formation_service")


class LoggerMixin:
    """Mixin class to add logging capabilities to classes"""

    @property
    def logger(self) -> structlog.BoundLoggerBase:
        """Get logger for this class"""
        class_name = self.__class__.__name__
        return get_logger(f"{class_name}")


def log_function_call(func):
    """Decorator to log function calls"""
    def wrapper(*args, **kwargs):
        logger = get_logger(f"{func.__module__}.{func.__qualname__}")
        logger.info(
            "Function called",
            function=func.__qualname__,
            args_count=len(args),
            kwargs_count=len(kwargs)
        )
        try:
            result = func(*args, **kwargs)
            logger.info(
                "Function completed",
                function=func.__qualname__,
                success=True
            )
            return result
        except Exception as e:
            logger.error(
                "Function failed",
                function=func.__qualname__,
                error=str(e),
                success=False
            )
            raise
    return wrapper


def log_api_request(func):
    """Decorator to log API requests"""
    async def wrapper(*args, **kwargs):
        logger = get_logger(f"{func.__module__}.{func.__qualname__}")
        logger.info(
            "API request started",
            function=func.__qualname__,
            method=func.__name__
        )
        try:
            result = await func(*args, **kwargs)
            logger.info(
                "API request completed",
                function=func.__qualname__,
                success=True
            )
            return result
        except Exception as e:
            logger.error(
                "API request failed",
                function=func.__qualname__,
                error=str(e),
                success=False
            )
            raise
    return wrapper
