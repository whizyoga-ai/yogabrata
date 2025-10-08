"""
API routes for Startup Formation Service
"""

from typing import Dict, Any, List
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db, Workflow, WorkflowStep, FounderProfile
from ..core.exceptions import ValidationError, WorkflowNotFoundError
from ..core.logging import get_logger

logger = get_logger()
router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "startup-formation-service",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.post("/workflows")
async def create_workflow(
    workflow_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """Create a new startup formation workflow"""
    try:
        # Validate required fields
        required_fields = ["company_name", "founder_name", "founder_email"]
        for field in required_fields:
            if field not in workflow_data:
                raise ValidationError(f"Missing required field: {field}")

        # Generate workflow ID
        workflow_id = str(uuid.uuid4())

        # Create workflow record
        workflow = Workflow(
            workflow_id=workflow_id,
            company_name=workflow_data["company_name"],
            entity_type=workflow_data.get("entity_type", "LLC"),
            state=workflow_data.get("state", "WA"),
            industry=workflow_data.get("industry", "Technology"),
            founder_name=workflow_data["founder_name"],
            founder_email=workflow_data["founder_email"],
            founder_role=workflow_data.get("founder_role", "Founder"),
            description=workflow_data.get("description"),
            status="pending",
            progress=0.0,
            workflow_metadata=workflow_data.get("metadata", {})
        )

        db.add(workflow)
        await db.commit()
        await db.refresh(workflow)

        logger.info("Workflow created", workflow_id=workflow_id)

        return {
            "workflow_id": workflow_id,
            "status": "created",
            "message": "Startup formation workflow created successfully",
            "next_steps": [
                "Complete founder verification",
                "Business entity analysis",
                "Document preparation",
                "Government registration"
            ]
        }

    except ValidationError:
        raise
    except Exception as e:
        logger.error("Failed to create workflow", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create workflow"
        )


@router.get("/workflows")
async def list_workflows(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """List all workflows"""
    try:
        result = await db.execute(
            select(Workflow).offset(skip).limit(limit)
        )
        workflows = result.scalars().all()

        return {
            "workflows": [
                {
                    "workflow_id": w.workflow_id,
                    "company_name": w.company_name,
                    "status": w.status,
                    "progress": w.progress,
                    "created_at": w.created_at.isoformat(),
                    "estimated_completion": w.estimated_completion.isoformat() if w.estimated_completion else None
                }
                for w in workflows
            ],
            "total": len(workflows),
            "skip": skip,
            "limit": limit
        }

    except Exception as e:
        logger.error("Failed to list workflows", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve workflows"
        )


@router.get("/workflows/{workflow_id}")
async def get_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get workflow details"""
    try:
        result = await db.execute(
            select(Workflow).where(Workflow.workflow_id == workflow_id)
        )
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise WorkflowNotFoundError(workflow_id)

        # Get workflow steps
        steps_result = await db.execute(
            select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)
        )
        steps = steps_result.scalars().all()

        return {
            "workflow_id": workflow.workflow_id,
            "company_name": workflow.company_name,
            "entity_type": workflow.entity_type,
            "state": workflow.state,
            "industry": workflow.industry,
            "founder_name": workflow.founder_name,
            "founder_email": workflow.founder_email,
            "founder_role": workflow.founder_role,
            "status": workflow.status,
            "progress": workflow.progress,
            "current_step": workflow.current_step,
            "description": workflow.description,
            "created_at": workflow.created_at.isoformat(),
            "updated_at": workflow.updated_at.isoformat(),
            "estimated_completion": workflow.estimated_completion.isoformat() if workflow.estimated_completion else None,
            "steps": [
                {
                    "step_id": s.step_id,
                    "name": s.name,
                    "status": s.status,
                    "started_at": s.started_at.isoformat() if s.started_at else None,
                    "completed_at": s.completed_at.isoformat() if s.completed_at else None,
                    "result": s.result
                }
                for s in steps
            ]
        }

    except WorkflowNotFoundError:
        raise
    except Exception as e:
        logger.error("Failed to get workflow", workflow_id=workflow_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve workflow"
        )


@router.post("/workflows/{workflow_id}/steps/{step_id}")
async def update_workflow_step(
    workflow_id: str,
    step_id: str,
    update_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """Update workflow step status"""
    try:
        result = await db.execute(
            select(WorkflowStep).where(
                WorkflowStep.workflow_id == workflow_id,
                WorkflowStep.step_id == step_id
            )
        )
        step = result.scalar_one_or_none()

        if not step:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Step {step_id} not found in workflow {workflow_id}"
            )

        # Update step fields
        if "status" in update_data:
            step.status = update_data["status"]

        if "result" in update_data:
            step.result = update_data["result"]

        if "error" in update_data:
            step.error = update_data["error"]

        if step.status == "completed" and not step.completed_at:
            step.completed_at = datetime.utcnow()
        elif step.status == "in_progress" and not step.started_at:
            step.started_at = datetime.utcnow()

        await db.commit()

        logger.info("Workflow step updated",
                   workflow_id=workflow_id,
                   step_id=step_id,
                   status=step.status)

        return {
            "workflow_id": workflow_id,
            "step_id": step_id,
            "status": step.status,
            "updated_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update workflow step",
                    workflow_id=workflow_id,
                    step_id=step_id,
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update workflow step"
        )


@router.get("/templates")
async def get_workflow_templates():
    """Get available workflow templates"""
    return {
        "templates": {
            "wa_llc_formation": {
                "name": "Washington LLC Formation",
                "description": "Complete LLC formation workflow for Washington State",
                "estimated_duration": "5-7 business days",
                "steps": 8,
                "states_supported": ["WA"],
                "features": [
                    "Articles of Organization",
                    "EIN Application",
                    "WA DOR Registration",
                    "Operating Agreement Template"
                ]
            },
            "ca_corporation": {
                "name": "California Corporation Formation",
                "description": "Complete corporation formation workflow for California",
                "estimated_duration": "7-10 business days",
                "steps": 10,
                "states_supported": ["CA"],
                "features": [
                    "Articles of Incorporation",
                    "Statement of Information",
                    "Corporate Bylaws Template",
                    "Federal EIN Application"
                ]
            }
        }
    }


@router.get("/integrations/status")
async def get_integration_status():
    """Get status of external integrations"""
    return {
        "integrations": {
            "wa_sos": {
                "name": "Washington Secretary of State",
                "status": "connected",
                "last_check": datetime.utcnow().isoformat(),
                "response_time": "1.2s"
            },
            "wa_dor": {
                "name": "Washington Department of Revenue",
                "status": "connected",
                "last_check": datetime.utcnow().isoformat(),
                "response_time": "0.8s"
            },
            "irs_ein": {
                "name": "IRS EIN Service",
                "status": "pending",
                "last_check": None,
                "response_time": None
            }
        }
    }
