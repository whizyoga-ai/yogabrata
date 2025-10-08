"""
Startup Formation Service - Main Application
Independent microservice for handling business formation workflows
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog
from dotenv import load_dotenv

from src.api.routes import router as api_router
from src.core.database import engine, Base, get_db
from src.core.config import settings
from src.core.logging import setup_logging
from src.core.exceptions import ServiceError

# Load environment variables
load_dotenv()

# Setup structured logging
setup_logging()
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI application
    Handles startup and shutdown events
    """
    logger.info("Starting Startup Formation Service")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created/verified")

    # Startup health checks would go here
    # - Database connectivity
    # - External API connections
    # - Message queue connections

    yield

    logger.info("Shutting down Startup Formation Service")

# Create FastAPI application
app = FastAPI(
    title="Startup Formation Service",
    description="Independent microservice for business formation workflows",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add trusted host middleware
if settings.TRUSTED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS
    )

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancer and monitoring"""
    return {
        "status": "healthy",
        "service": "startup-formation-service",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/readiness")
async def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    # Add actual readiness checks here
    # - Database connectivity
    # - External service availability
    return {"status": "ready"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Startup Formation Service API",
        "docs": "/docs",
        "health": "/health"
    }

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    """Handle service-specific errors"""
    logger.error("Service error", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "message": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error("Unexpected error", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "message": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server", host="0.0.0.0", port=8000)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        log_config=None,  # Use our structured logging
        access_log=True
    )
