"""
Business Formation Agent for Yogabrata Platform

Specialized AI agent for helping users launch startups with Washington State compliance.
Integrates with WA DOR and SOS MCP servers for real-time business registration guidance.
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, TaskContext, AgentResponse

class BusinessFormationAgent(BaseAgent):
    """AI agent specialized in business formation and Washington State compliance"""

    def __init__(self, mcp_manager):
        super().__init__(
            name="business_formation",
            description="AI agent for startup launch and Washington State business compliance",
            mcp_manager=mcp_manager
        )

        # Add specific capabilities
        self.add_capability("business_registration")
        self.add_capability("wa_state_compliance")
        self.add_capability("business_structure_advisory")
        self.add_capability("license_requirements")
        self.add_capability("tax_setup_guidance")

    def get_required_mcp_servers(self) -> List[str]:
        """Required MCP servers for business formation"""
        return ["wa_dor", "wa_sos", "legal_us"]

    async def process_task(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Process business formation related tasks"""

        task_lower = task.lower()

        # Route to appropriate handler based on task content
        if any(keyword in task_lower for keyword in ["register", "incorporate", "form", "start"]):
            return await self._handle_business_registration(task, context)
        elif any(keyword in task_lower for keyword in ["license", "permit", "certification"]):
            return await self._handle_license_requirements(task, context)
        elif any(keyword in task_lower for keyword in ["tax", "taxes", "ein", "federal tax"]):
            return await self._handle_tax_setup(task, context)
        elif any(keyword in task_lower for keyword in ["structure", "llc", "corporation", "partnership"]):
            return await self._handle_business_structure(task, context)
        elif any(keyword in task_lower for keyword in ["compliance", "requirements", "regulations"]):
            return await self._handle_compliance_check(task, context)
        else:
            return await self._handle_general_inquiry(task, context)

    async def _handle_business_registration(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Handle business registration tasks"""

        # Query Washington State SOS for current registration info
        sos_data = await self.query_mcp_servers(
            "business registration requirements Washington state",
            ["wa_sos"]
        )

        # Query DOR for tax registration requirements
        dor_data = await self.query_mcp_servers(
            "business tax registration requirements Washington state",
            ["wa_dor"]
        )

        # Analyze business type from task
        business_type = self._extract_business_type(task)

        response_data = {
            "business_type": business_type,
            "registration_steps": self._get_registration_steps(business_type),
            "wa_sos_info": sos_data.get("wa_sos", {}),
            "wa_dor_info": dor_data.get("wa_dor", {}),
            "estimated_timeline": "2-4 weeks",
            "estimated_cost": "$200-500",
            "required_documents": self._get_required_documents(business_type)
        }

        return {
            "success": True,
            "data": response_data,
            "message": f"Business registration guidance for {business_type} in Washington State",
            "mcp_sources": ["wa_sos", "wa_dor"]
        }

    async def _handle_license_requirements(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Handle license and permit requirements"""

        # Extract business type and industry
        business_info = self._extract_business_info(task)

        # Query relevant servers for license requirements
        license_data = await self.query_mcp_servers(
            f"business license requirements for {business_info.get('industry', 'general business')} in Washington state",
            ["wa_sos", "legal_us"]
        )

        response_data = {
            "business_type": business_info.get("type", "unknown"),
            "industry": business_info.get("industry", "general"),
            "required_licenses": self._get_licenses_for_business(business_info),
            "wa_sos_data": license_data.get("wa_sos", {}),
            "legal_requirements": license_data.get("legal_us", {}),
            "application_process": "Apply through Washington State Business Licensing Service"
        }

        return {
            "success": True,
            "data": response_data,
            "message": f"License requirements for {business_info.get('industry', 'your business')} in Washington State",
            "mcp_sources": ["wa_sos", "legal_us"]
        }

    async def _handle_tax_setup(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Handle tax setup and registration"""

        # Query DOR for tax requirements
        tax_data = await self.query_mcp_servers(
            "business tax setup requirements Washington state",
            ["wa_dor"]
        )

        response_data = {
            "tax_obligations": [
                "Washington State Business & Occupation (B&O) Tax",
                "Retail Sales Tax (if selling goods)",
                "Use Tax (if buying items for business use)",
                "Property Tax (for business property)",
                "Federal EIN (Employer Identification Number)"
            ],
            "registration_requirements": tax_data.get("wa_dor", {}),
            "filing_frequency": "Monthly, Quarterly, or Annual based on tax liability",
            "estimated_setup_time": "1-2 weeks",
            "resources": {
                "wa_dor_website": "https://dor.wa.gov",
                "ein_application": "https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online"
            }
        }

        return {
            "success": True,
            "data": response_data,
            "message": "Tax setup guidance for Washington State businesses",
            "mcp_sources": ["wa_dor"]
        }

    async def _handle_business_structure(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Handle business structure recommendations"""

        # Analyze task for business characteristics
        business_characteristics = self._analyze_business_characteristics(task)

        # Get structure recommendations
        recommendations = self._get_structure_recommendations(business_characteristics)

        response_data = {
            "recommended_structures": recommendations,
            "factors_considered": business_characteristics,
            "legal_considerations": "Liability protection, tax implications, formation requirements",
            "next_steps": "Consult with legal professional for final determination"
        }

        return {
            "success": True,
            "data": response_data,
            "message": "Business structure recommendations based on your requirements",
            "mcp_sources": ["legal_us"]
        }

    async def _handle_compliance_check(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Handle compliance checking tasks"""

        # Query multiple sources for compliance requirements
        compliance_data = await self.query_mcp_servers(
            "business compliance requirements Washington state",
            ["wa_sos", "wa_dor", "legal_us"]
        )

        response_data = {
            "compliance_areas": [
                "Business Registration",
                "Tax Compliance",
                "Employment Laws",
                "Industry-Specific Regulations",
                "Annual Reporting Requirements"
            ],
            "wa_sos_compliance": compliance_data.get("wa_sos", {}),
            "wa_dor_compliance": compliance_data.get("wa_dor", {}),
            "federal_compliance": compliance_data.get("legal_us", {}),
            "monitoring_schedule": "Monthly compliance review recommended"
        }

        return {
            "success": True,
            "data": response_data,
            "message": "Washington State business compliance requirements",
            "mcp_sources": ["wa_sos", "wa_dor", "legal_us"]
        }

    async def _handle_general_inquiry(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Handle general business formation inquiries"""

        # Query all available sources for general guidance
        general_data = await self.query_mcp_servers(
            f"business formation guidance: {task}",
            ["wa_sos", "wa_dor", "legal_us"]
        )

        response_data = {
            "inquiry_type": "general",
            "guidance_sources": list(general_data.keys()),
            "recommendation": "Consider consulting with a business attorney or accountant for personalized advice",
            "resources": {
                "wa_business_licensing": "https://bls.dor.wa.gov/",
                "sos_business_search": "https://ccfs.sos.wa.gov/",
                "small_business_administration": "https://www.sba.gov/"
            }
        }

        return {
            "success": True,
            "data": response_data,
            "message": "General business formation guidance",
            "mcp_sources": list(general_data.keys())
        }

    def _extract_business_type(self, task: str) -> str:
        """Extract business type from task description"""
        task_lower = task.lower()

        if any(word in task_lower for word in ["llc", "limited liability"]):
            return "LLC"
        elif any(word in task_lower for word in ["corporation", "corp", "inc"]):
            return "Corporation"
        elif any(word in task_lower for word in ["partnership", "llp"]):
            return "Partnership"
        elif any(word in task_lower for word in ["nonprofit", "501c3"]):
            return "Nonprofit"
        else:
            return "LLC"  # Default recommendation

    def _extract_business_info(self, task: str) -> Dict[str, str]:
        """Extract business type and industry from task"""
        return {
            "type": self._extract_business_type(task),
            "industry": self._extract_industry(task)
        }

    def _extract_industry(self, task: str) -> str:
        """Extract industry from task description"""
        industries = [
            "technology", "software", "consulting", "retail", "restaurant",
            "healthcare", "manufacturing", "real estate", "professional services"
        ]

        task_lower = task.lower()
        for industry in industries:
            if industry in task_lower:
                return industry

        return "general business"

    def _analyze_business_characteristics(self, task: str) -> Dict[str, Any]:
        """Analyze business characteristics for structure recommendations"""
        characteristics = {
            "liability_concerns": "high" if "high risk" in task.lower() else "medium",
            "growth_plans": "aggressive" if any(word in task.lower() for word in ["scale", "grow", "expand"]) else "moderate",
            "ownership_structure": "multiple" if any(word in task.lower() for word in ["partners", "multiple owners"]) else "single",
            "industry_risk": "high" if any(word in task.lower() for word in ["healthcare", "construction", "manufacturing"]) else "low"
        }
        return characteristics

    def _get_registration_steps(self, business_type: str) -> List[str]:
        """Get registration steps for business type"""
        base_steps = [
            "Choose and reserve business name",
            "File formation documents with WA Secretary of State",
            "Obtain Unified Business Identifier (UBI) number",
            "Register for business license through BLS",
            "Apply for federal Employer Identification Number (EIN)"
        ]

        if business_type == "Corporation":
            base_steps.insert(2, "File Articles of Incorporation")
        elif business_type == "LLC":
            base_steps.insert(2, "File Certificate of Formation")
        elif business_type == "Partnership":
            base_steps.insert(2, "File partnership registration")

        return base_steps

    def _get_required_documents(self, business_type: str) -> List[str]:
        """Get required documents for business type"""
        documents = [
            "Valid government-issued photo ID",
            "Social Security Number or EIN",
            "Business address in Washington State",
            "Contact information (phone, email)"
        ]

        if business_type == "Corporation":
            documents.append("Articles of Incorporation")
        elif business_type == "LLC":
            documents.append("Certificate of Formation")
        elif business_type == "Partnership":
            documents.append("Partnership Agreement")

        return documents

    def _get_licenses_for_business(self, business_info: Dict[str, str]) -> List[Dict[str, str]]:
        """Get required licenses for business type and industry"""
        licenses = [
            {
                "name": "Washington State Business License",
                "agency": "Washington State Department of Revenue",
                "required": "Yes",
                "description": "Required for all businesses operating in Washington State"
            }
        ]

        industry = business_info.get("industry", "").lower()

        if industry in ["restaurant", "food service"]:
            licenses.append({
                "name": "Food Service Permit",
                "agency": "Local Health Department",
                "required": "Yes",
                "description": "Required for food preparation and service"
            })
        elif industry in ["healthcare", "medical"]:
            licenses.append({
                "name": "Healthcare Professional License",
                "agency": "Washington State Department of Health",
                "required": "Yes",
                "description": "Required for healthcare providers"
            })

        return licenses

    def _get_structure_recommendations(self, characteristics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get business structure recommendations based on characteristics"""
        recommendations = []

        # LLC recommendation
        if characteristics.get("liability_concerns") in ["high", "medium"]:
            recommendations.append({
                "structure": "LLC",
                "score": 85,
                "reasons": ["Limited liability protection", "Flexible management structure"],
                "considerations": ["Self-employment taxes", "Formation costs"]
            })

        # Corporation recommendation
        if characteristics.get("growth_plans") == "aggressive":
            recommendations.append({
                "structure": "Corporation",
                "score": 80,
                "reasons": ["Easier to raise capital", "Established structure for growth"],
                "considerations": ["More complex compliance", "Double taxation potential"]
            })

        # Partnership recommendation
        if characteristics.get("ownership_structure") == "multiple":
            recommendations.append({
                "structure": "Partnership",
                "score": 70,
                "reasons": ["Simple to establish", "Shared management"],
                "considerations": ["Unlimited personal liability", "Partnership agreement required"]
            })

        # Sort by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)

        return recommendations
