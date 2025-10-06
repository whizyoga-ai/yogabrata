"""
MCP (Model Context Protocol) Manager for Yogabrata Platform

Manages connections to external MCP servers for government, legal, and business data.
Provides a unified interface for AI agents to access real-time information.
"""

import asyncio
import logging
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from contextlib import asynccontextmanager

try:
    from mcp import ClientSession, stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logging.warning("MCP library not available. Install with: pip install mcp")
    # Create dummy classes to prevent import errors
    class ClientSession:
        pass
    def stdio_client(*args, **kwargs):
        return None

import httpx
from bs4 import BeautifulSoup
import json

@dataclass
class MCPServerConfig:
    """Configuration for an MCP server connection"""
    name: str
    server_type: str  # 'mcp', 'api', 'web_scraping'
    connection_url: str
    authentication: Optional[Dict[str, Any]] = None
    rate_limit: int = 10  # requests per minute
    timeout: int = 30

class MCPServerConnection:
    """Represents a connection to an MCP server"""

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.session = None
        self.last_request = 0
        self.request_count = 0

    async def connect(self) -> bool:
        """Establish connection to the MCP server"""
        try:
            if self.config.server_type == 'mcp' and MCP_AVAILABLE:
                # MCP protocol connection
                self.session = ClientSession()
                # Implementation depends on MCP library specifics
                return True

            elif self.config.server_type == 'api':
                # HTTP API connection
                return await self._test_api_connection()

            elif self.config.server_type == 'web_scraping':
                # Web scraping connection
                return await self._test_web_connection()

            return False
        except Exception as e:
            logging.error(f"Failed to connect to {self.config.name}: {e}")
            return False

    async def _test_api_connection(self) -> bool:
        """Test HTTP API connection"""
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(self.config.connection_url)
                return response.status_code < 400
        except Exception:
            return False

    async def _test_web_connection(self) -> bool:
        """Test web scraping connection"""
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(self.config.connection_url)
                return response.status_code == 200
        except Exception:
            return False

    async def query(self, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Query the MCP server"""
        # Rate limiting
        current_time = asyncio.get_event_loop().time()
        if current_time - self.last_request < 60 / self.config.rate_limit:
            await asyncio.sleep(60 / self.config.rate_limit - (current_time - self.last_request))

        self.last_request = asyncio.get_event_loop().time()
        self.request_count += 1

        try:
            if self.config.server_type == 'api':
                return await self._query_api(query, params)
            elif self.config.server_type == 'web_scraping':
                return await self._query_web_scraping(query, params)
            else:
                return {"error": "Unsupported server type"}
        except Exception as e:
            logging.error(f"Query failed for {self.config.name}: {e}")
            return {"error": str(e)}

    async def _query_api(self, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Query HTTP API"""
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                self.config.connection_url,
                json={"query": query, "params": params},
                headers=self.config.authentication or {}
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API returned status {response.status_code}"}

    async def _query_web_scraping(self, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Query via web scraping"""
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.get(self.config.connection_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract relevant data based on query
                return {
                    "content": soup.get_text(),
                    "title": soup.title.string if soup.title else "",
                    "url": self.config.connection_url
                }
            else:
                return {"error": f"Web request failed with status {response.status_code}"}

class MCPManager:
    """Main MCP Manager for handling multiple server connections"""

    def __init__(self):
        self.connections: Dict[str, MCPServerConnection] = {}
        self._initialize_servers()

    def _initialize_servers(self):
        """Initialize connections to known MCP servers"""

        # Washington State Department of Revenue
        self.add_server(MCPServerConfig(
            name="wa_dor",
            server_type="web_scraping",
            connection_url="https://dor.wa.gov/businesses",
            rate_limit=5
        ))

        # Washington Secretary of State
        self.add_server(MCPServerConfig(
            name="wa_sos",
            server_type="web_scraping",
            connection_url="https://sos.wa.gov/businesses",
            rate_limit=5
        ))

        # USPTO (United States Patent and Trademark Office)
        self.add_server(MCPServerConfig(
            name="uspto",
            server_type="api",
            connection_url="https://developer.uspto.gov/api",
            rate_limit=20
        ))

        # Grants.gov
        self.add_server(MCPServerConfig(
            name="grants_gov",
            server_type="api",
            connection_url="https://www.grants.gov/web/grants/search-grants.html",
            rate_limit=10
        ))

        # Legal compliance data (placeholder)
        self.add_server(MCPServerConfig(
            name="legal_us",
            server_type="web_scraping",
            connection_url="https://www.usa.gov/business-laws",
            rate_limit=15
        ))

    def add_server(self, config: MCPServerConfig):
        """Add a new MCP server connection"""
        self.connections[config.name] = MCPServerConnection(config)

    async def connect_all(self) -> Dict[str, bool]:
        """Connect to all configured servers"""
        results = {}
        for name, connection in self.connections.items():
            results[name] = await connection.connect()
        return results

    async def query_server(self, server_name: str, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Query a specific server"""
        if server_name not in self.connections:
            return {"error": f"Server '{server_name}' not found"}

        return await self.connections[server_name].query(query, params)

    async def query_multiple(self, server_names: List[str], query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Query multiple servers concurrently"""
        tasks = []
        for server_name in server_names:
            if server_name in self.connections:
                tasks.append(self.connections[server_name].query(query, params))

        if not tasks:
            return {"error": "No valid servers specified"}

        results = await asyncio.gather(*tasks, return_exceptions=True)

        response = {}
        for i, server_name in enumerate(server_names):
            if i < len(results):
                response[server_name] = results[i] if not isinstance(results[i], Exception) else {"error": str(results[i])}

        return response

    def get_server_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all servers"""
        status = {}
        for name, connection in self.connections.items():
            status[name] = {
                "connected": connection.session is not None,
                "request_count": connection.request_count,
                "last_request": connection.last_request,
                "config": {
                    "server_type": connection.config.server_type,
                    "rate_limit": connection.config.rate_limit,
                    "timeout": connection.config.timeout
                }
            }
        return status

# Global MCP manager instance
mcp_manager = MCPManager()
