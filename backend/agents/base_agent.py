"""
Base Agent Class for Yogabrata AI Platform

Provides the foundation for all specialized AI agents with MCP integration.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from core.mcp_manager import MCPManager

@dataclass
class AgentResponse:
    """Standardized response from AI agents"""
    success: bool
    data: Dict[str, Any]
    message: str
    agent_name: str
    execution_time: float
    mcp_sources: List[str]
    timestamp: datetime

@dataclass
class TaskContext:
    """Context information for agent tasks"""
    user_id: str
    task_id: str
    priority: int = 1
    metadata: Optional[Dict[str, Any]] = None

class BaseAgent(ABC):
    """Abstract base class for all AI agents"""

    def __init__(self, name: str, description: str, mcp_manager: MCPManager):
        self.name = name
        self.description = description
        self.mcp_manager = mcp_manager
        self.capabilities: List[str] = []
        self.is_active = False
        self.logger = logging.getLogger(f"agent.{name}")

    async def initialize(self) -> bool:
        """Initialize the agent and its MCP connections"""
        try:
            self.logger.info(f"Initializing agent: {self.name}")

            # Connect to required MCP servers
            connection_results = await self.mcp_manager.connect_all()

            # Check if all required servers are connected
            required_servers = self.get_required_mcp_servers()
            missing_servers = [
                server for server in required_servers
                if server not in connection_results or not connection_results[server]
            ]

            if missing_servers:
                self.logger.warning(f"Missing connections for servers: {missing_servers}")
                # Continue anyway - some servers might be optional

            self.is_active = True
            self.logger.info(f"Agent {self.name} initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize agent {self.name}: {e}")
            return False

    @abstractmethod
    def get_required_mcp_servers(self) -> List[str]:
        """Return list of required MCP server names for this agent"""
        pass

    @abstractmethod
    async def process_task(self, task: str, context: TaskContext) -> AgentResponse:
        """Process a task and return response"""
        pass

    async def execute_task(self, task: str, context: TaskContext) -> AgentResponse:
        """Execute a task with timing and error handling"""
        start_time = datetime.now()

        try:
            self.logger.info(f"Executing task for agent {self.name}: {task[:100]}...")

            if not self.is_active:
                await self.initialize()

            # Process the task
            result = await self.process_task(task, context)

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            # Create response
            response = AgentResponse(
                success=result.get("success", False),
                data=result.get("data", {}),
                message=result.get("message", ""),
                agent_name=self.name,
                execution_time=execution_time,
                mcp_sources=result.get("mcp_sources", []),
                timestamp=datetime.now()
            )

            self.logger.info(f"Task completed in {execution_time:.2f}s")
            return response

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Task failed after {execution_time:.2f}s: {e}")

            return AgentResponse(
                success=False,
                data={"error": str(e)},
                message=f"Task failed: {str(e)}",
                agent_name=self.name,
                execution_time=execution_time,
                mcp_sources=[],
                timestamp=datetime.now()
            )

    async def query_mcp_servers(self, query: str, server_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Query MCP servers for information"""
        if server_names:
            return await self.mcp_manager.query_multiple(server_names, query)
        else:
            # Query all available servers
            required_servers = self.get_required_mcp_servers()
            return await self.mcp_manager.query_multiple(required_servers, query)

    def get_status(self) -> Dict[str, Any]:
        """Get agent status and health information"""
        return {
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "capabilities": self.capabilities,
            "mcp_servers": self.get_required_mcp_servers(),
            "mcp_status": self.mcp_manager.get_server_status()
        }

    def add_capability(self, capability: str):
        """Add a capability to this agent"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)

    def remove_capability(self, capability: str):
        """Remove a capability from this agent"""
        if capability in self.capabilities:
            self.capabilities.remove(capability)
