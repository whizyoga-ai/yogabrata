"""
Mock MCP Servers for Startup Formation Workflow

This module provides mock implementations of various government and legal
MCP servers for testing and development purposes.
"""

import asyncio
import json
import random
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MockMCPServer:
    """Base class for mock MCP servers"""

    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.is_connected = False
        self.response_delay = random.uniform(0.5, 2.0)  # Simulate network delay

    async def connect(self) -> bool:
        """Simulate connection to MCP server"""
        await asyncio.sleep(0.5)
        self.is_connected = True
        logger.info(f"Connected to {self.name} MCP server")
        return True

    async def disconnect(self):
        """Simulate disconnection from MCP server"""
        await asyncio.sleep(0.2)
        self.is_connected = False
        logger.info(f"Disconnected from {self.name} MCP server")

    async def query(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Query the MCP server"""
        if not self.is_connected:
            raise ConnectionError(f"{self.name} server not connected")

        await asyncio.sleep(self.response_delay)

        # Route to appropriate handler based on endpoint
        if endpoint == "/name-availability":
            return await self.check_name_availability(params)
        elif endpoint == "/business-registration":
            return await self.register_business(params)
        elif endpoint == "/file-articles":
            return await self.file_articles(params)
        elif endpoint == "/tax-accounts":
            return await self.setup_tax_accounts(params)
        elif endpoint == "/legal-compliance":
            return await self.check_legal_compliance(params)
        else:
            return {"error": "Unknown endpoint", "endpoint": endpoint}

    async def check_name_availability(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock name availability check"""
        business_name = params.get("name", "")
        state = params.get("state", "WA")

        # Simulate some names being taken
        taken_names = ["Apple", "Google", "Microsoft", "Amazon", "Tesla"]
        name_taken = any(taken_name.lower() in business_name.lower() for taken_name in taken_names)

        return {
            "available": not name_taken,
            "name": business_name,
            "state": state,
            "alternatives": [
                f"{business_name} LLC",
                f"{business_name} Technologies",
                f"{business_name} Solutions",
                f"{business_name} Innovations"
            ] if name_taken else [],
            "checked_at": datetime.now().isoformat(),
            "server": self.name
        }

    async def register_business(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock business registration"""
        return {
            "registration_id": f"REG{random.randint(100000, 999999)}",
            "status": "processing",
            "estimated_completion": (datetime.now() + timedelta(days=7)).isoformat(),
            "documents_required": ["Articles of Organization", "Operating Agreement"],
            "filing_fee": 200.00,
            "state": params.get("state", "WA"),
            "server": self.name
        }

    async def file_articles(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock articles of organization filing"""
        return {
            "filing_number": f"ART{random.randint(1000000, 9999999)}",
            "filed_at": datetime.now().isoformat(),
            "status": "accepted",
            "processing_time": "5-7 business days",
            "next_steps": [
                "Wait for approval notification",
                "Obtain Certificate of Formation",
                "Apply for EIN"
            ],
            "server": self.name
        }

    async def setup_tax_accounts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock tax account setup"""
        return {
            "tax_accounts": [
                {
                    "type": "Business & Occupation Tax",
                    "account_number": f"BO{random.randint(100000, 999999)}",
                    "status": "active"
                },
                {
                    "type": "Sales Tax",
                    "account_number": f"ST{random.randint(100000, 999999)}",
                    "status": "active"
                }
            ],
            "quarterly_filing_dates": [
                "January 31",
                "April 30",
                "July 31",
                "October 31"
            ],
            "setup_completed": datetime.now().isoformat(),
            "server": self.name
        }

    async def check_legal_compliance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock legal compliance check"""
        return {
            "compliant": True,
            "requirements_met": [
                "Business name available",
                "Articles prepared correctly",
                "Registered agent designated",
                "State filing requirements met"
            ],
            "next_compliance_dates": [
                {
                    "type": "Annual Report",
                    "due_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
                },
                {
                    "type": "Tax Filing",
                    "due_date": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                }
            ],
            "server": self.name
        }


class WashingtonSOSServer(MockMCPServer):
    """Mock Washington Secretary of State MCP Server"""

    def __init__(self):
        super().__init__("wa_sos", "https://sos.wa.gov")

    async def check_name_availability(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """WA SOS specific name availability"""
        result = await super().check_name_availability(params)

        # Add WA-specific requirements
        result.update({
            "wa_distinguishable": result["available"],
            "wa_name_rules": [
                "Must contain LLC, L.L.C., or Limited Liability Company",
                "Cannot imply government affiliation",
                "Must be distinguishable from existing entities"
            ],
            "wa_sos_contact": "sos.ca.gov",
            "processing_time": "1-2 business days"
        })

        return result

    async def file_articles(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """WA SOS specific filing"""
        result = await super().file_articles(params)

        result.update({
            "wa_sos_filing": True,
            "certificate_issuance": (datetime.now() + timedelta(days=5)).isoformat(),
            "wa_sos_tracking": f"WA{random.randint(1000000, 9999999)}",
            "expedited_service_available": True,
            "expedited_fee": 50.00
        })

        return result


class WashingtonDORServer(MockMCPServer):
    """Mock Washington Department of Revenue MCP Server"""

    def __init__(self):
        super().__init__("wa_dor", "https://dor.wa.gov")

    async def register_business(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """WA DOR specific business registration"""
        result = await super().register_business(params)

        result.update({
            "wa_dor_registration": True,
            "tax_obligations": [
                "Business & Occupation (B&O) Tax",
                "Sales Tax (if selling goods)",
                "Use Tax (if using goods in business)"
            ],
            "wa_dor_account_number": f"DOR{random.randint(100000, 999999)}",
            "first_return_due": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "dor_contact": "dor.wa.gov"
        })

        return result

    async def setup_tax_accounts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """WA DOR specific tax account setup"""
        result = await super().setup_tax_accounts(params)

        result.update({
            "wa_dor_accounts": True,
            "bo_tax_rate": "0.471% for most businesses",
            "quarterly_returns": True,
            "electronic_filing_required": True,
            "wa_dor_website": "dor.wa.gov"
        })

        return result


class LegalComplianceServer(MockMCPServer):
    """Mock Legal Compliance MCP Server"""

    def __init__(self):
        super().__init__("legal_us", "https://legal.gov")

    async def check_legal_compliance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Legal compliance checking"""
        business_type = params.get("entity_type", "LLC")
        state = params.get("state", "WA")

        return {
            "compliant": True,
            "federal_requirements": [
                "Obtain EIN from IRS",
                "File annual reports if applicable",
                "Maintain proper business records",
                "Comply with employment laws if hiring"
            ],
            "state_requirements": [
                f"Washington State {business_type} requirements",
                "Annual report filing",
                "State tax registration",
                "Business license requirements"
            ],
            "industry_specific": [
                "General business compliance",
                "Contract requirements",
                "Insurance recommendations"
            ],
            "next_steps": [
                "Review operating agreement",
                "Set up business banking",
                "Consider business insurance",
                "Plan for annual compliance"
            ],
            "server": self.name
        }


class IRSMockServer(MockMCPServer):
    """Mock IRS MCP Server for EIN applications"""

    def __init__(self):
        super().__init__("irs", "https://irs.gov")

    async def apply_for_ein(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock EIN application"""
        await asyncio.sleep(self.response_delay)

        return {
            "ein": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
            "application_method": "Online",
            "processing_time": "Immediate",
            "confirmation_number": f"EIN{random.randint(100000, 999999)}",
            "next_steps": [
                "Save EIN confirmation",
                "Use for business banking",
                "Update business records"
            ],
            "server": self.name
        }


class MCPMockServerManager:
    """Manager for all mock MCP servers"""

    def __init__(self):
        self.servers: Dict[str, MockMCPServer] = {
            "wa_sos": WashingtonSOSServer(),
            "wa_dor": WashingtonDORServer(),
            "legal_us": LegalComplianceServer(),
            "irs": IRSMockServer()
        }
        self.connected_servers: List[str] = []

    async def connect_all(self) -> Dict[str, bool]:
        """Connect to all available MCP servers"""
        results = {}

        for server_name, server in self.servers.items():
            try:
                success = await server.connect()
                results[server_name] = success
                if success:
                    self.connected_servers.append(server_name)
            except Exception as e:
                logger.error(f"Failed to connect to {server_name}: {e}")
                results[server_name] = False

        return results

    async def disconnect_all(self):
        """Disconnect from all MCP servers"""
        for server in self.servers.values():
            await server.disconnect()
        self.connected_servers.clear()

    async def query_server(self, server_name: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Query a specific MCP server"""
        if server_name not in self.servers:
            return {"error": f"Server {server_name} not found"}

        server = self.servers[server_name]
        if not server.is_connected:
            return {"error": f"Server {server_name} not connected"}

        try:
            return await server.query(endpoint, params)
        except Exception as e:
            return {"error": f"Query failed: {str(e)}"}

    async def get_server_status(self) -> Dict[str, Any]:
        """Get status of all servers"""
        return {
            server_name: {
                "connected": server.is_connected,
                "name": server.name,
                "base_url": server.base_url
            }
            for server_name, server in self.servers.items()
        }

    def get_available_servers(self) -> List[str]:
        """Get list of available server names"""
        return list(self.servers.keys())


# Global instance for easy access
mock_mcp_manager = MCPMockServerManager()


async def initialize_mock_servers():
    """Initialize all mock MCP servers"""
    logger.info("Initializing mock MCP servers...")
    results = await mock_mcp_manager.connect_all()

    connected = sum(results.values())
    total = len(results)

    logger.info(f"Connected to {connected}/{total} mock MCP servers")

    if connected == 0:
        logger.warning("No MCP servers connected - workflow may not function properly")

    return results


if __name__ == "__main__":
    # Test the mock servers
    async def test_servers():
        await initialize_mock_servers()

        # Test name availability
        result = await mock_mcp_manager.query_server("wa_sos", "/name-availability", {
            "name": "Test Business LLC",
            "state": "WA"
        })
        print("Name availability result:", json.dumps(result, indent=2))

        # Test business registration
        result = await mock_mcp_manager.query_server("wa_dor", "/business-registration", {
            "business_name": "Test Business LLC",
            "state": "WA"
        })
        print("Business registration result:", json.dumps(result, indent=2))

    asyncio.run(test_servers())
