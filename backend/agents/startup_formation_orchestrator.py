"""
Startup Formation Orchestrator Agent

Coordinates the end-to-end startup formation workflow with multi-founder support,
dynamic role detection, and comprehensive state management.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

from .base_agent import BaseAgent, TaskContext, AgentResponse
from core.mcp_manager import MCPManager

class FounderRole(Enum):
    CEO = "ceo"
    CFO = "cfo"
    CTO = "cto"
    FOUNDER = "founder"
    OTHER = "other"

class WorkflowStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class FounderInfo:
    """Information about a startup founder"""
    name: str
    email: str
    role: FounderRole
    ownership_percentage: float
    responsibilities: List[str]

@dataclass
class CompanyInfo:
    """Information about the company being formed"""
    name: str
    entity_type: str  # LLC, Corporation, Partnership, etc.
    state: str
    industry: str
    description: str
    founders: List[FounderInfo]

@dataclass
class WorkflowStep:
    """Individual step in the startup formation workflow"""
    step_id: str
    name: str
    description: str
    assigned_roles: List[FounderRole]
    status: WorkflowStatus
    dependencies: List[str]  # step_ids this step depends on
    estimated_duration: int  # minutes
    actual_duration: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class WorkflowState:
    """Complete state of a startup formation workflow"""
    workflow_id: str
    company_info: CompanyInfo
    status: WorkflowStatus
    steps: Dict[str, WorkflowStep]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    current_step: Optional[str] = None
    progress_percentage: float = 0.0

class StartupFormationOrchestrator(BaseAgent):
    """Main orchestrator for startup formation workflows"""

    def __init__(self, mcp_manager: MCPManager):
        super().__init__(
            name="startup_formation_orchestrator",
            description="Coordinates end-to-end startup formation with multi-founder support",
            mcp_manager=mcp_manager
        )

        self.active_workflows: Dict[str, WorkflowState] = {}
        self.workflow_templates: Dict[str, List[WorkflowStep]] = {}

        # Initialize workflow templates
        self._initialize_workflow_templates()

        # Add capabilities
        self.add_capability("workflow_orchestration")
        self.add_capability("multi_founder_management")
        self.add_capability("business_entity_registration")
        self.add_capability("compliance_automation")
        self.add_capability("visual_workflow_display")

    async def initialize(self) -> bool:
        """Initialize the agent with fault-tolerant MCP connections"""
        try:
            self.logger.info(f"Initializing agent: {self.name}")

            # Try to connect to required MCP servers but don't fail if some are unavailable
            try:
                connection_results = await self.mcp_manager.connect_all()
                self.logger.info(f"MCP connection results: {connection_results}")
            except Exception as e:
                self.logger.warning(f"MCP connection failed, continuing anyway: {e}")

            # Check if required servers are available
            required_servers = self.get_required_mcp_servers()
            available_servers = [
                server for server in required_servers
                if server in self.mcp_manager.connections
            ]

            if available_servers:
                self.logger.info(f"Available MCP servers: {available_servers}")
            else:
                self.logger.warning("No required MCP servers available")

            # Mark as active even if some servers are unavailable
            self.is_active = True
            self.logger.info(f"Agent {self.name} initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize agent {self.name}: {e}")
            # Still mark as active to allow operation with limited functionality
            self.is_active = True
            return True

    def _initialize_workflow_templates(self):
        """Initialize standard workflow templates for different company types"""

        # LLC Formation Template
        llc_steps = [
            WorkflowStep(
                step_id="analyze_requirements",
                name="Analyze Business Requirements",
                description="Analyze founder information and determine optimal business structure",
                assigned_roles=[FounderRole.CEO, FounderRole.FOUNDER],
                status=WorkflowStatus.PENDING,
                dependencies=[],
                estimated_duration=15
            ),
            WorkflowStep(
                step_id="name_availability",
                name="Check Name Availability",
                description="Verify business name availability across state and federal databases",
                assigned_roles=[FounderRole.CEO],
                status=WorkflowStatus.PENDING,
                dependencies=["analyze_requirements"],
                estimated_duration=10
            ),
            WorkflowStep(
                step_id="prepare_articles",
                name="Prepare Articles of Organization",
                description="Generate and prepare Articles of Organization for filing",
                assigned_roles=[FounderRole.CEO],
                status=WorkflowStatus.PENDING,
                dependencies=["name_availability"],
                estimated_duration=20
            ),
            WorkflowStep(
                step_id="file_state_registration",
                name="File State Registration",
                description="Submit registration documents to Secretary of State",
                assigned_roles=[FounderRole.CEO],
                status=WorkflowStatus.PENDING,
                dependencies=["prepare_articles"],
                estimated_duration=30
            ),
            WorkflowStep(
                step_id="obtain_ein",
                name="Obtain EIN",
                description="Apply for Employer Identification Number from IRS",
                assigned_roles=[FounderRole.CFO],
                status=WorkflowStatus.PENDING,
                dependencies=["file_state_registration"],
                estimated_duration=25
            ),
            WorkflowStep(
                step_id="setup_business_banking",
                name="Setup Business Banking",
                description="Establish business banking relationship and accounts",
                assigned_roles=[FounderRole.CFO],
                status=WorkflowStatus.PENDING,
                dependencies=["obtain_ein"],
                estimated_duration=45
            ),
            WorkflowStep(
                step_id="register_state_taxes",
                name="Register for State Taxes",
                description="Register with state revenue department for tax obligations",
                assigned_roles=[FounderRole.CFO],
                status=WorkflowStatus.PENDING,
                dependencies=["file_state_registration"],
                estimated_duration=20
            ),
            WorkflowStep(
                step_id="setup_payroll",
                name="Setup Payroll System",
                description="Configure payroll and HR systems for employee management",
                assigned_roles=[FounderRole.CFO],
                status=WorkflowStatus.PENDING,
                dependencies=["obtain_ein"],
                estimated_duration=35
            ),
            WorkflowStep(
                step_id="compliance_setup",
                name="Initial Compliance Setup",
                description="Establish compliance monitoring and reporting systems",
                assigned_roles=[FounderRole.CFO],
                status=WorkflowStatus.PENDING,
                dependencies=["file_state_registration"],
                estimated_duration=30
            ),
            WorkflowStep(
                step_id="generate_operating_agreement",
                name="Generate Operating Agreement",
                description="Create comprehensive operating agreement for the LLC",
                assigned_roles=[FounderRole.CEO],
                status=WorkflowStatus.PENDING,
                dependencies=["file_state_registration"],
                estimated_duration=40
            )
        ]

        self.workflow_templates["llc"] = llc_steps

        # Corporation Formation Template (similar structure)
        corp_steps = [
            WorkflowStep(
                step_id="analyze_requirements",
                name="Analyze Corporate Requirements",
                description="Analyze founder information and determine corporate structure",
                assigned_roles=[FounderRole.CEO, FounderRole.FOUNDER],
                status=WorkflowStatus.PENDING,
                dependencies=[],
                estimated_duration=20
            ),
            # ... additional corporation-specific steps
        ]

        self.workflow_templates["corporation"] = corp_steps

    def get_required_mcp_servers(self) -> List[str]:
        """Return required MCP servers for startup formation"""
        return [
            "wa_sos",      # Washington Secretary of State
            "wa_dor",      # Washington Department of Revenue
            "legal_us",    # Legal compliance data
        ]

    async def process_task(self, task: str, context: TaskContext) -> Dict[str, Any]:
        """Process startup formation tasks"""

        try:
            # Parse the task to understand the request
            task_data = self._parse_task_request(task)

            if task_data["action"] == "create_startup":
                return await self._create_startup_workflow(task_data, context)
            elif task_data["action"] == "check_status":
                return await self._check_workflow_status(task_data, context)
            elif task_data["action"] == "get_workflow_visualization":
                return await self._get_workflow_visualization(task_data, context)
            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {task_data['action']}",
                    "data": {}
                }

        except Exception as e:
            self.logger.error(f"Error processing task: {e}")
            return {
                "success": False,
                "message": f"Task processing failed: {str(e)}",
                "data": {"error": str(e)}
            }

    def _parse_task_request(self, task: str) -> Dict[str, Any]:
        """Parse task string to extract structured request data"""
        # This is a simplified parser - in production, use proper NLP or structured input
        task_lower = task.lower()

        if "create startup" in task_lower or "form company" in task_lower:
            return {"action": "create_startup"}
        elif "check status" in task_lower or "workflow status" in task_lower:
            return {"action": "check_status"}
        elif "visualization" in task_lower or "flowchart" in task_lower:
            return {"action": "get_workflow_visualization"}
        else:
            return {"action": "unknown"}

    async def _create_startup_workflow(self, task_data: Dict[str, Any], context: TaskContext) -> Dict[str, Any]:
        """Create a new startup formation workflow"""

        # For now, create a sample company - in production, extract from task/context
        company_info = CompanyInfo(
            name="Sample Tech LLC",
            entity_type="llc",
            state="washington",
            industry="technology",
            description="A technology consulting and development company",
            founders=[
                FounderInfo(
                    name="John Doe",
                    email="john@sampletech.com",
                    role=FounderRole.CEO,
                    ownership_percentage=50.0,
                    responsibilities=["business_strategy", "operations"]
                ),
                FounderInfo(
                    name="Jane Smith",
                    email="jane@sampletech.com",
                    role=FounderRole.CFO,
                    ownership_percentage=50.0,
                    responsibilities=["finance", "compliance"]
                )
            ]
        )

        # Create workflow ID
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Initialize workflow state
        workflow_state = WorkflowState(
            workflow_id=workflow_id,
            company_info=company_info,
            status=WorkflowStatus.IN_PROGRESS,
            steps={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Add workflow steps based on entity type
        template_steps = self.workflow_templates.get(company_info.entity_type.lower(), self.workflow_templates["llc"])

        for step in template_steps:
            # Create a copy of the step for this workflow
            workflow_step = WorkflowStep(
                step_id=step.step_id,
                name=step.name,
                description=step.description,
                assigned_roles=step.assigned_roles,
                status=WorkflowStatus.PENDING,
                dependencies=step.dependencies,
                estimated_duration=step.estimated_duration
            )
            workflow_state.steps[step.step_id] = workflow_step

        # Start the first step
        await self._start_next_workflow_step(workflow_state)

        # Store the workflow
        self.active_workflows[workflow_id] = workflow_state

        # Start workflow execution in background
        asyncio.create_task(self._execute_workflow(workflow_id, context))

        return {
            "success": True,
            "message": f"Startup formation workflow created: {workflow_id}",
            "data": {
                "workflow_id": workflow_id,
                "company_name": company_info.name,
                "entity_type": company_info.entity_type,
                "estimated_completion": self._calculate_estimated_completion(workflow_state),
                "next_steps": self._get_next_steps(workflow_state)
            }
        }

    async def _execute_workflow(self, workflow_id: str, context: TaskContext):
        """Execute the complete workflow asynchronously"""
        if workflow_id not in self.active_workflows:
            return

        workflow_state = self.active_workflows[workflow_id]

        try:
            while True:
                # Find the next step to execute
                next_step = self._find_next_executable_step(workflow_state)
                if not next_step:
                    break

                # Execute the step
                await self._execute_workflow_step(workflow_id, next_step.step_id, context)

                # Update progress
                self._update_workflow_progress(workflow_state)

                # Check if workflow is complete
                if workflow_state.status == WorkflowStatus.COMPLETED:
                    break

                # Small delay between steps
                await asyncio.sleep(1)

        except Exception as e:
            self.logger.error(f"Workflow execution failed for {workflow_id}: {e}")
            workflow_state.status = WorkflowStatus.FAILED
            workflow_state.updated_at = datetime.now()

    def _find_next_executable_step(self, workflow_state: WorkflowState) -> Optional[WorkflowStep]:
        """Find the next step that can be executed"""
        for step in workflow_state.steps.values():
            if (step.status == WorkflowStatus.PENDING and
                self._check_dependencies_met(step, workflow_state)):
                return step
        return None

    def _check_dependencies_met(self, step: WorkflowStep, workflow_state: WorkflowState) -> bool:
        """Check if all dependencies for a step are met"""
        for dep_id in step.dependencies:
            if dep_id in workflow_state.steps:
                dep_step = workflow_state.steps[dep_id]
                if dep_step.status != WorkflowStatus.COMPLETED:
                    return False
        return True

    async def _execute_workflow_step(self, workflow_id: str, step_id: str, context: TaskContext):
        """Execute a specific workflow step"""
        if workflow_id not in self.active_workflows:
            return

        workflow_state = self.active_workflows[workflow_id]
        step = workflow_state.steps[step_id]

        # Mark step as in progress
        step.status = WorkflowStatus.IN_PROGRESS
        step.started_at = datetime.now()
        workflow_state.current_step = step_id
        workflow_state.updated_at = datetime.now()

        try:
            # Execute the step based on its type
            result = await self._execute_step_action(step, workflow_state, context)

            # Mark step as completed
            step.status = WorkflowStatus.COMPLETED
            step.completed_at = datetime.now()
            step.result = result

            # Calculate actual duration
            if step.started_at:
                duration = datetime.now() - step.started_at
                step.actual_duration = int(duration.total_seconds() / 60)

        except Exception as e:
            step.status = WorkflowStatus.FAILED
            step.error = str(e)
            step.completed_at = datetime.now()
            workflow_state.status = WorkflowStatus.FAILED

    async def _execute_step_action(self, step: WorkflowStep, workflow_state: WorkflowState, context: TaskContext) -> Dict[str, Any]:
        """Execute the specific action for a workflow step"""

        if step.step_id == "analyze_requirements":
            return await self._analyze_business_requirements(workflow_state)
        elif step.step_id == "name_availability":
            return await self._check_name_availability(workflow_state)
        elif step.step_id == "prepare_articles":
            return await self._prepare_articles_of_organization(workflow_state)
        elif step.step_id == "file_state_registration":
            return await self._file_state_registration(workflow_state)
        elif step.step_id == "obtain_ein":
            return await self._obtain_ein(workflow_state)
        elif step.step_id == "setup_business_banking":
            return await self._setup_business_banking(workflow_state)
        elif step.step_id == "register_state_taxes":
            return await self._register_state_taxes(workflow_state)
        elif step.step_id == "setup_payroll":
            return await self._setup_payroll_system(workflow_state)
        elif step.step_id == "compliance_setup":
            return await self._setup_compliance_monitoring(workflow_state)
        elif step.step_id == "generate_operating_agreement":
            return await self._generate_operating_agreement(workflow_state)
        else:
            return await self._execute_mcp_step(step, workflow_state)

    async def _analyze_business_requirements(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Analyze business requirements and recommend structure"""
        company = workflow_state.company_info

        # Query MCP servers for business structure recommendations
        mcp_results = await self.query_mcp_servers(
            f"Analyze business structure for {company.industry} {company.entity_type} in {company.state}",
            ["wa_sos", "legal_us"]
        )

        return {
            "recommended_structure": company.entity_type,
            "state_requirements": "Washington State LLC requirements",
            "federal_requirements": "Standard federal business requirements",
            "mcp_sources": list(mcp_results.keys())
        }

    async def _check_name_availability(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Check business name availability"""
        company = workflow_state.company_info

        # Query state SOS for name availability
        mcp_results = await self.query_mcp_servers(
            f"Check availability of business name: {company.name}",
            ["wa_sos"]
        )

        return {
            "name_available": True,  # Mock response
            "alternatives": [f"{company.name} LLC", f"{company.name} Technologies"],
            "search_results": mcp_results,
            "mcp_sources": list(mcp_results.keys())
        }

    async def _prepare_articles_of_organization(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Prepare Articles of Organization"""
        company = workflow_state.company_info

        # Generate articles document
        articles = {
            "company_name": company.name,
            "entity_type": company.entity_type,
            "registered_agent": "Yogabrata Legal Services",
            "principal_office": "Washington State",
            "organizers": [founder.name for founder in company.founders],
            "management_structure": "Member-managed"
        }

        return {
            "articles_prepared": True,
            "document_id": f"articles_{workflow_state.workflow_id}",
            "articles_content": articles,
            "filing_fee": 200.00
        }

    async def _file_state_registration(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """File state registration documents"""
        # Mock filing with Secretary of State
        return {
            "filing_submitted": True,
            "filing_number": f"WA{datetime.now().strftime('%Y%m%d')}{workflow_state.workflow_id[-6:]}",
            "filing_date": datetime.now().isoformat(),
            "expected_processing_time": "5-7 business days",
            "status_url": "https://sos.wa.gov/business-filings-status"
        }

    async def _obtain_ein(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Obtain EIN from IRS"""
        # Mock EIN application
        return {
            "ein_obtained": True,
            "ein_number": f"{datetime.now().strftime('%Y%m%d')}{workflow_state.workflow_id[-6:]}",
            "application_method": "Online application",
            "processing_time": "Immediate"
        }

    async def _setup_business_banking(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Setup business banking"""
        return {
            "banking_setup": True,
            "recommended_banks": ["Chase", "Bank of America", "Wells Fargo"],
            "account_types": ["Business checking", "Business savings"],
            "next_steps": "Contact bank with EIN and Articles of Organization"
        }

    async def _register_state_taxes(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Register for state taxes"""
        return {
            "tax_registration": True,
            "tax_accounts": ["Business & Occupation Tax", "Sales Tax"],
            "registration_numbers": [f"WA{workflow_state.workflow_id[-8:]}1", f"WA{workflow_state.workflow_id[-8:]}2"],
            "quarterly_filing_dates": ["Jan 31", "Apr 30", "Jul 31", "Oct 31"]
        }

    async def _setup_payroll_system(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Setup payroll system"""
        return {
            "payroll_configured": True,
            "system_recommendations": ["Gusto", "ADP", "Paychex"],
            "setup_steps": ["Create company profile", "Add employees", "Configure payroll schedule"],
            "estimated_monthly_cost": "$40-150 depending on provider"
        }

    async def _setup_compliance_monitoring(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Setup compliance monitoring"""
        return {
            "compliance_setup": True,
            "monitoring_areas": ["Annual reports", "Tax filings", "License renewals"],
            "alert_schedule": "Monthly compliance review",
            "reporting_dashboard": "Available at yogabrata.com/dashboard"
        }

    async def _generate_operating_agreement(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Generate operating agreement"""
        company = workflow_state.company_info

        agreement = {
            "agreement_type": "Operating Agreement",
            "company_name": company.name,
            "members": [
                {
                    "name": founder.name,
                    "role": founder.role.value,
                    "ownership_percentage": founder.ownership_percentage
                }
                for founder in company.founders
            ],
            "management_structure": "Member-managed",
            "profit_distribution": "Proportional to ownership",
            "meeting_requirements": "Annual member meetings"
        }

        return {
            "agreement_generated": True,
            "document_id": f"oa_{workflow_state.workflow_id}",
            "sections": list(agreement.keys()),
            "customization_needed": True
        }

    def _update_workflow_progress(self, workflow_state: WorkflowState):
        """Update overall workflow progress"""
        total_steps = len(workflow_state.steps)
        completed_steps = sum(1 for step in workflow_state.steps.values() if step.status == WorkflowStatus.COMPLETED)

        workflow_state.progress_percentage = (completed_steps / total_steps) * 100

        if completed_steps == total_steps:
            workflow_state.status = WorkflowStatus.COMPLETED
            workflow_state.completed_at = datetime.now()

        workflow_state.updated_at = datetime.now()

    def _calculate_estimated_completion(self, workflow_state: WorkflowState) -> str:
        """Calculate estimated completion time"""
        remaining_steps = [step for step in workflow_state.steps.values()
                          if step.status != WorkflowStatus.COMPLETED]

        if not remaining_steps:
            return "Completed"

        total_estimated_minutes = sum(step.estimated_duration for step in remaining_steps)
        estimated_completion = datetime.now() + timedelta(minutes=total_estimated_minutes)

        return estimated_completion.strftime("%Y-%m-%d %H:%M:%S")

    def _get_next_steps(self, workflow_state: WorkflowState) -> List[str]:
        """Get list of next steps for the user"""
        next_steps = []

        for step in workflow_state.steps.values():
            if step.status == WorkflowStatus.PENDING:
                next_steps.append(f"{step.name}: {step.description}")

        return next_steps[:3]  # Return top 3 next steps

    async def _start_next_workflow_step(self, workflow_state: WorkflowState):
        """Start the next available workflow step"""
        next_step = self._find_next_executable_step(workflow_state)
        if next_step:
            next_step.status = WorkflowStatus.IN_PROGRESS
            next_step.started_at = datetime.now()
            workflow_state.current_step = next_step.step_id

    async def _check_workflow_status(self, task_data: Dict[str, Any], context: TaskContext) -> Dict[str, Any]:
        """Check status of a workflow"""
        workflow_id = task_data.get("workflow_id")

        if not workflow_id or workflow_id not in self.active_workflows:
            return {
                "success": False,
                "message": "Workflow not found",
                "data": {}
            }

        workflow_state = self.active_workflows[workflow_id]

        return {
            "success": True,
            "message": f"Workflow status: {workflow_state.status.value}",
            "data": {
                "workflow_id": workflow_id,
                "status": workflow_state.status.value,
                "progress_percentage": workflow_state.progress_percentage,
                "current_step": workflow_state.current_step,
                "created_at": workflow_state.created_at.isoformat(),
                "estimated_completion": self._calculate_estimated_completion(workflow_state),
                "next_steps": self._get_next_steps(workflow_state),
                "completed_steps": sum(1 for step in workflow_state.steps.values() if step.status == WorkflowStatus.COMPLETED),
                "total_steps": len(workflow_state.steps)
            }
        }

    async def _get_workflow_visualization(self, task_data: Dict[str, Any], context: TaskContext) -> Dict[str, Any]:
        """Get workflow visualization data"""
        workflow_id = task_data.get("workflow_id")

        if workflow_id and workflow_id in self.active_workflows:
            workflow_state = self.active_workflows[workflow_id]
        else:
            # Return template visualization
            workflow_state = None

        # Generate Mermaid diagram
        mermaid_diagram = self._generate_mermaid_diagram(workflow_state)

        return {
            "success": True,
            "message": "Workflow visualization generated",
            "data": {
                "mermaid_diagram": mermaid_diagram,
                "workflow_id": workflow_id,
                "entity_type": workflow_state.company_info.entity_type if workflow_state else "llc",
                "total_steps": len(workflow_state.steps) if workflow_state else len(self.workflow_templates["llc"]),
                "format": "mermaid"
            }
        }

    def _generate_mermaid_diagram(self, workflow_state: Optional[WorkflowState]) -> str:
        """Generate Mermaid diagram for workflow visualization"""

        if workflow_state:
            steps = workflow_state.steps
            company_name = workflow_state.company_info.name
        else:
            steps = self.workflow_templates["llc"]
            company_name = "Sample Company"

        diagram = f"""graph TD
    A[Start: {company_name} Formation] --> B[Analyze Requirements]
    B --> C[Check Name Availability]
    C --> D[Prepare Articles]
    D --> E[File State Registration]
    E --> F[Obtain EIN]
    E --> G[Register State Taxes]
    F --> H[Setup Business Banking]
    F --> I[Setup Payroll System]
    E --> J[Setup Compliance]
    D --> K[Generate Operating Agreement]
    H --> L[Formation Complete]
    I --> L
    G --> L
    J --> L
    K --> L

    classDef pending fill:#f9f9f9,stroke:#333,stroke-width:2px
    classDef in_progress fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef completed fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef failed fill:#ffebee,stroke:#c62828,stroke-width:2px
"""

        if workflow_state:
            for step in steps.values():
                if step.status == WorkflowStatus.COMPLETED:
                    diagram += f"    class {step.step_id.replace('_', '').upper()} completed\n"
                elif step.status == WorkflowStatus.IN_PROGRESS:
                    diagram += f"    class {step.step_id.replace('_', '').upper()} in_progress\n"
                elif step.status == WorkflowStatus.FAILED:
                    diagram += f"    class {step.step_id.replace('_', '').upper()} failed\n"
                else:
                    diagram += f"    class {step.step_id.replace('_', '').upper()} pending\n"

        return diagram

    def get_workflow_summary(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of a workflow for display"""
        if workflow_id not in self.active_workflows:
            return None

        workflow_state = self.active_workflows[workflow_id]

        return {
            "workflow_id": workflow_id,
            "company_name": workflow_state.company_info.name,
            "status": workflow_state.status.value,
            "progress": workflow_state.progress_percentage,
            "current_step": workflow_state.current_step,
            "created_at": workflow_state.created_at.isoformat(),
            "estimated_completion": self._calculate_estimated_completion(workflow_state)
        }

    def list_active_workflows(self) -> List[Dict[str, Any]]:
        """List all active workflows"""
        return [
            self.get_workflow_summary(wf_id)
            for wf_id in self.active_workflows.keys()
        ]

    async def _execute_mcp_step(self, step: WorkflowStep, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Execute a step that requires MCP server interaction"""
        company = workflow_state.company_info

        # Determine which MCP servers to query based on the step
        mcp_servers = []
        endpoint = ""

        if "name_availability" in step.step_id:
            mcp_servers = ["wa_sos"]
            endpoint = "/name-availability"
        elif "registration" in step.step_id:
            mcp_servers = ["wa_dor", "wa_sos"]
            endpoint = "/business-registration"
        elif "tax" in step.step_id:
            mcp_servers = ["wa_dor"]
            endpoint = "/tax-accounts"
        elif "compliance" in step.step_id:
            mcp_servers = ["legal_us"]
            endpoint = "/legal-compliance"
        else:
            # Generic MCP query
            mcp_servers = ["wa_sos", "wa_dor", "legal_us"]
            endpoint = "/query"

        # Query MCP servers
        try:
            mcp_results = await self.query_mcp_servers(
                f"Execute {step.name} for {company.name}",
                mcp_servers
            )

            return {
                "mcp_servers_queried": mcp_servers,
                "endpoint": endpoint,
                "results": mcp_results,
                "step_completed": True,
                "company_name": company.name,
                "entity_type": company.entity_type,
                "state": company.state
            }

        except Exception as e:
            self.logger.error(f"MCP step execution failed for {step.step_id}: {e}")
            return {
                "error": f"MCP server interaction failed: {str(e)}",
                "mcp_servers": mcp_servers,
                "step_failed": True
            }
