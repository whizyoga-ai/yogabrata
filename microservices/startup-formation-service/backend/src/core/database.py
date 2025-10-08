"""
Database configuration and session management for Startup Formation Service
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Text, Boolean, JSON, Float
from datetime import datetime
import structlog

from .config import settings

logger = structlog.get_logger()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=10,
    max_overflow=20,
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()


# Database Models

class Workflow(Base):
    """Main workflow model for tracking startup formation processes"""
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # LLC, Corporation, etc.
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    industry: Mapped[str] = mapped_column(String(100), nullable=False)

    # Founder information
    founder_name: Mapped[str] = mapped_column(String(255), nullable=False)
    founder_email: Mapped[str] = mapped_column(String(255), nullable=False)
    founder_role: Mapped[str] = mapped_column(String(100), nullable=False)

    # Workflow status
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, in_progress, completed, failed
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    current_step: Mapped[str] = mapped_column(String(100), nullable=True)

    # Business description
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estimated_completion: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Metadata
    workflow_metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class WorkflowStep(Base):
    """Individual steps within a workflow"""
    __tablename__ = "workflow_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    step_id: Mapped[str] = mapped_column(String(100), nullable=False)

    # Step information
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, in_progress, completed, failed, skipped

    # Step execution
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    estimated_duration: Mapped[int] = mapped_column(Integer, nullable=True)  # minutes
    actual_duration: Mapped[int] = mapped_column(Integer, nullable=True)  # minutes

    # Step results
    result: Mapped[dict] = mapped_column(JSON, default=dict)
    error: Mapped[str] = mapped_column(Text, nullable=True)

    # Dependencies
    depends_on: Mapped[list] = mapped_column(JSON, default=list)  # List of step_ids this step depends on

    # Order
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)

    # Metadata
    step_metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class FounderProfile(Base):
    """Founder information and verification status"""
    __tablename__ = "founder_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    # Personal information
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    role: Mapped[str] = mapped_column(String(100), nullable=False)  # CEO, CTO, Founder, etc.

    # Verification status
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    address_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Verification timestamps
    email_verified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    identity_verified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    address_verified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Metadata
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CompanyEntity(Base):
    """Business entity information"""
    __tablename__ = "company_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    # Entity information
    entity_name: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    state_of_formation: Mapped[str] = mapped_column(String(50), nullable=False)

    # Registration details
    registration_number: Mapped[str] = mapped_column(String(100), nullable=True)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    registration_status: Mapped[str] = mapped_column(String(50), nullable=True)

    # Tax information
    ein: Mapped[str] = mapped_column(String(20), nullable=True)  # Employer Identification Number
    tax_id: Mapped[str] = mapped_column(String(50), nullable=True)
    tax_status: Mapped[str] = mapped_column(String(50), nullable=True)

    # Business addresses
    principal_address: Mapped[dict] = mapped_column(JSON, nullable=True)  # Full address object
    mailing_address: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Metadata
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Document(Base):
    """Generated documents for workflows"""
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    # Document information
    document_type: Mapped[str] = mapped_column(String(100), nullable=False)  # articles_of_organization, operating_agreement, etc.
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)

    # Document status
    status: Mapped[str] = mapped_column(String(50), default="generating")  # generating, ready, error
    file_size: Mapped[int] = mapped_column(Integer, nullable=True)  # bytes

    # Generation details
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    template_used: Mapped[str] = mapped_column(String(255), nullable=True)
    generation_error: Mapped[str] = mapped_column(Text, nullable=True)

    # Document content (for simple documents)
    content: Mapped[Text] = mapped_column(Text, nullable=True)

    # Metadata
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class IntegrationLog(Base):
    """Logs for external API integrations"""
    __tablename__ = "integration_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    # Integration details
    integration_name: Mapped[str] = mapped_column(String(100), nullable=False)  # wa_sos, irs, etc.
    endpoint: Mapped[str] = mapped_column(String(500), nullable=False)
    method: Mapped[str] = mapped_column(String(10), nullable=False)  # GET, POST, etc.

    # Request/Response
    request_payload: Mapped[dict] = mapped_column(JSON, nullable=True)
    response_payload: Mapped[dict] = mapped_column(JSON, nullable=True)
    response_status: Mapped[int] = mapped_column(Integer, nullable=True)

    # Timing
    request_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    response_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=True)

    # Status
    success: Mapped[bool] = mapped_column(Boolean, default=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)

    # Metadata
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# Create all tables (for development)
async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


# Drop all tables (for testing)
async def drop_tables():
    """Drop all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped successfully")
