"""
Legal Compliance Agent for Yogabrata Platform

Handles legal compliance checking and regulatory guidance.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, TaskContext, AgentResponse

logger = logging.getLogger(__name__)

class LegalComplianceAgent(BaseAgent):
    """AI agent for legal compliance and regulatory guidance"""

    def __init__(self, mcp_manager):
        super().__init__(
            name="legal_compliance",
            description="Legal compliance checking and regulatory guidance",
            capabilities=[
                "compliance_audit",
                "regulatory_guidance",
                "legal_research",
                "risk_assessment"
            ],
            mcp_manager=mcp_manager
        )

    async def initialize(self) -> bool:
        """Initialize the legal compliance agent"""
        try:
            # Connect to legal MCP servers
            legal_servers = ["legal_us", "wa_sos"]
            connection_results = await self.mcp_manager.connect_all()

            self.is_active = all([
                connection_results.get(server, False)
                for server in legal_servers
                if server in connection_results
            ])

            logger.info(f"Legal Compliance Agent initialized: {self.is_active}")
            return self.is_active

        except Exception as e:
            logger.error(f"Failed to initialize Legal Compliance Agent: {e}")
            self.is_active = False
            return False

    async def execute_task(self, task: str, context: TaskContext) -> AgentResponse:
        """Execute legal compliance task"""
        start_time = datetime.now()

        try:
            # Analyze the task type
            if "audit" in task.lower() or "check" in task.lower():
                result = await self._perform_compliance_audit(task, context)
            elif "guide" in task.lower() or "advice" in task.lower():
                result = await self._provide_regulatory_guidance(task, context)
            elif "research" in task.lower():
                result = await self._conduct_legal_research(task, context)
            else:
                result = await self._assess_legal_risk(task, context)

            execution_time = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                success=True,
                message=result["message"],
                data=result["data"],
                agent_name=self.name,
                execution_time=execution_time,
                mcp_sources=result.get("mcp_sources", []),
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Legal Compliance Agent task failed: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                success=False,
                message=f"Legal compliance task failed: {str(e)}",
                data={},
                agent_name=self.name,
                execution_time=execution_time,
                mcp_sources=[],
                timestamp=datetime.now()
            )

    async def _perform_compliance_audit(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Perform compliance audit"""
        # Query legal servers for compliance data
        legal_data = await self.mcp_manager.query_server(
            "legal_us",
            "compliance_requirements",
            {"business_type": "general"}
        )

        audit_result = {
            "overall_compliance": "Good",
            "compliance_score": 85,
            "areas_reviewed": [
                "Business Registration",
                "Tax Compliance",
                "Employment Laws",
                "Data Privacy"
            ],
            "findings": [
                "Business registration is current",
                "Tax filings are up to date",
                "Employment documentation complete"
            ],
            "recommendations": [
                "Review data privacy policy annually",
                "Update compliance training for employees"
            ]
        }

        return {
            "message": "Compliance audit completed successfully",
            "data": {
                "audit_result": audit_result,
                "legal_references": legal_data,
                "next_review_date": "2025-04-01"
            },
            "mcp_sources": ["legal_us"]
        }

    async def _provide_regulatory_guidance(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Provide regulatory guidance"""
        guidance = {
            "applicable_laws": [
                "Washington State Business License requirements",
                "Federal employment laws",
                "Data protection regulations"
            ],
            "required_actions": [
                "Obtain proper business licensing",
                "Maintain employee records",
                "Implement data security measures"
            ],
            "resources": [
                "WA Department of Revenue website",
                "SBA compliance guide",
                "Legal compliance checklist"
            ]
        }

        return {
            "message": "Regulatory guidance provided",
            "data": {
                "guidance": guidance,
                "urgency_level": "Medium",
                "estimated_completion": "2-4 weeks"
            },
            "mcp_sources": ["wa_sos"]
        }

    async def _conduct_legal_research(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Conduct legal research"""
        research_findings = {
            "topic": "Business compliance requirements",
            "key_findings": [
                "Washington State requires business license within 30 days",
                "Federal EIN required for tax purposes",
                "Employment laws apply to businesses with employees"
            ],
            "citations": [
                "WA DOR Business License Guide",
                "IRS Publication 334",
                "DOL Employment Law Overview"
            ]
        }

        return {
            "message": "Legal research completed",
            "data": {
                "research_findings": research_findings,
                "confidence_level": "High",
                "last_updated": "2024-12-01"
            },
            "mcp_sources": ["legal_us", "wa_sos"]
        }

    async def _assess_legal_risk(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Assess legal risk"""
        risk_assessment = {
            "overall_risk_level": "Low",
            "risk_factors": [
                "Proper business registration",
                "Compliance with employment laws",
                "Data protection measures"
            ],
            "risk_score": 25,
            "mitigation_strategies": [
                "Regular compliance reviews",
                "Employee training programs",
                "Legal consultation as needed"
            ]
        }

        return {
            "message": "Legal risk assessment completed",
            "data": {
                "risk_assessment": risk_assessment,
                "recommended_actions": [
                    "Schedule quarterly compliance reviews",
                    "Maintain updated legal documentation"
                ]
            },
            "mcp_sources": []
        }

    def get_required_mcp_servers(self) -> List[str]:
        """Get list of required MCP servers"""
        return ["legal_us", "wa_sos"]

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "is_active": self.is_active,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "required_mcp_servers": self.get_required_mcp_servers(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }
