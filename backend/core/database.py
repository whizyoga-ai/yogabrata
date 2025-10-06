"""
Database configuration and models for Yogabrata Platform
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./yogabrata.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    """User model for authentication and tracking"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class TaskExecution(Base):
    """Track AI agent task executions"""
    __tablename__ = "task_executions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    agent_name = Column(String, index=True)
    task_description = Column(Text)
    status = Column(String)  # pending, running, completed, failed
    result = Column(JSON)
    execution_time = Column(Integer)  # milliseconds
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class MCPConnection(Base):
    """Track MCP server connections and health"""
    __tablename__ = "mcp_connections"

    id = Column(Integer, primary_key=True, index=True)
    server_name = Column(String, unique=True, index=True)
    server_type = Column(String)
    connection_url = Column(String)
    is_connected = Column(Boolean, default=False)
    last_connection_attempt = Column(DateTime, default=datetime.utcnow)
    last_successful_connection = Column(DateTime, nullable=True)
    connection_errors = Column(JSON, default=list)

class AgentActivity(Base):
    """Track AI agent activities and performance"""
    __tablename__ = "agent_activities"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, index=True)
    activity_type = Column(String)  # initialized, task_executed, error
    description = Column(Text)
    agent_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on startup
def init_db():
    """Initialize database with tables"""
    try:
        create_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise
