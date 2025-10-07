"""
Yogabrata.com - Multi-Service AI Platform API

FastAPI backend with MCP integration for AI-powered business services.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# Import our custom modules
from core.mcp_manager import mcp_manager
from core.database import init_db
from agents.base_agent import BaseAgent, TaskContext, AgentResponse
from agents.business_formation_agent import BusinessFormationAgent
from agents.content_strategy_agent import ContentStrategyAgent
from agents.legal_compliance_agent import LegalComplianceAgent
from agents.startup_formation_orchestrator import StartupFormationOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent registry
agents: Dict[str, BaseAgent] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Yogabrata AI Platform...")

    # Initialize Database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

    # Initialize MCP Manager
    try:
        connection_results = await mcp_manager.connect_all()
        logger.info(f"MCP Manager initialized. Connection results: {connection_results}")
    except Exception as e:
        logger.error(f"Failed to initialize MCP Manager: {e}")

    # Initialize AI Agents
    try:
        # Startup Formation Orchestrator (Primary Agent)
        orchestrator = StartupFormationOrchestrator(mcp_manager)
        await orchestrator.initialize()
        agents["startup_orchestrator"] = orchestrator
        logger.info("Startup Formation Orchestrator initialized successfully")

        # Business Formation Agent
        business_agent = BusinessFormationAgent(mcp_manager)
        await business_agent.initialize()
        agents["business_formation"] = business_agent
        logger.info("Business Formation Agent initialized successfully")

        # Content Strategy Agent
        content_agent = ContentStrategyAgent(mcp_manager)
        await content_agent.initialize()
        agents["content_strategy"] = content_agent
        logger.info("Content Strategy Agent initialized successfully")

        # Legal Compliance Agent
        legal_agent = LegalComplianceAgent(mcp_manager)
        await legal_agent.initialize()
        agents["legal_compliance"] = legal_agent
        logger.info("Legal Compliance Agent initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize AI agents: {e}")

    yield

    # Shutdown
    logger.info("Shutting down Yogabrata AI Platform...")

# Create FastAPI app with lifespan management
app = FastAPI(
    title="Yogabrata AI Platform API",
    description="Multi-Service AI Platform with MCP Integration for Business Services",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Yogabrata AI Platform API</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1000px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
            .service-card { background: rgba(255,255,255,0.2); padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #4CAF50; }
            .endpoint { background: rgba(0,0,0,0.3); padding: 10px; margin: 10px 0; border-radius: 5px; font-family: monospace; }
            .mcp-status { background: rgba(76, 175, 80, 0.2); padding: 10px; border-radius: 5px; margin: 10px 0; }
            h1 { color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            h2 { color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
            a { color: #81C784; text-decoration: none; font-weight: bold; }
            a:hover { color: #A5D6A7; }
            .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #4CAF50; margin-right: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Yogabrata AI Platform API</h1>
            <p style="font-size: 18px; margin-bottom: 30px;">
                Multi-Service AI Platform with MCP Integration for Intelligent Business Services
            </p>

            <div class="mcp-status">
                <h3><span class="status-indicator"></span>MCP Integration Status</h3>
                <p>✅ MCP Manager Active | 🔗 Government Servers Connected | 🤖 AI Agents Ready</p>
            </div>

            <h2>🎯 Available AI Services</h2>

            <div class="service-card">
                <h3>🚀 Complete Startup Formation (NEW)</h3>
                <p>End-to-end AI-powered startup formation with multi-founder support, workflow orchestration, and visual progress tracking.</p>
                <strong>Agent:</strong> Startup Formation Orchestrator<br>
                <strong>Features:</strong> Multi-state registration, EIN automation, payroll setup, compliance monitoring<br>
                <strong>Status:</strong> <span style="color: #4CAF50;">✅ Active</span>
            </div>

            <div class="service-card">
                <h3>🏢 Business Formation (WA State)</h3>
                <p>Get AI-powered guidance for business formation, registration, and Washington State compliance.</p>
                <strong>Agent:</strong> Business Formation Agent<br>
                <strong>MCP Sources:</strong> WA DOR, WA SOS, Legal Compliance
            </div>

            <div class="service-card">
                <h3>⚖️ Legal Compliance Assistant</h3>
                <p>Automated legal compliance checking and regulatory guidance for businesses.</p>
                <strong>Agent:</strong> Legal Compliance Agent<br>
                <strong>MCP Sources:</strong> Federal Legal, State Regulations
            </div>

            <div class="service-card">
                <h3>💼 Market Research & Intelligence</h3>
                <p>AI-powered market analysis and business intelligence gathering.</p>
                <strong>Agent:</strong> Market Intelligence Agent<br>
                <strong>MCP Sources:</strong> Industry Data, Market Trends
            </div>

            <h2>🔌 API Endpoints</h2>
            <div class="endpoint">
                <strong>GET /</strong> - This information page
            </div>
            <div class="endpoint">
                <strong>GET /docs</strong> - Interactive API documentation (Swagger UI)
            </div>
            <div class="endpoint">
                <strong>GET /health</strong> - System health check
            </div>
            <div class="endpoint">
                <strong>POST /api/v2/agents/{agent_name}/execute</strong> - Execute AI agent tasks
            </div>
            <div class="endpoint">
                <strong>GET /api/v2/mcp/status</strong> - MCP server connection status
            </div>

            <h3>🚀 Startup Formation Endpoints</h3>
            <div class="endpoint">
                <strong>POST /api/v2/startup/create</strong> - Create new startup formation workflow
            </div>
            <div class="endpoint">
                <strong>GET /api/v2/startup/workflows</strong> - List all active workflows
            </div>
            <div class="endpoint">
                <strong>GET /api/v2/startup/workflows/{workflow_id}</strong> - Get workflow status
            </div>
            <div class="endpoint">
                <strong>POST /api/v2/startup/workflows/{workflow_id}/visualization</strong> - Get workflow visualization
            </div>
            <div class="endpoint">
                <strong>GET /api/v2/startup/templates</strong> - Get available workflow templates
            </div>

            <h2>🚀 Quick Start</h2>
            <p>Visit <a href="/docs">/docs</a> for interactive API documentation</p>
            <p>Test MCP connections: <a href="/api/v2/mcp/status">/api/v2/mcp/status</a></p>

            <h2>💡 Example Usage</h2>
            <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto;">
curl -X POST "http://localhost:8000/api/v2/agents/business_formation/execute" \\
  -H "Content-Type: application/json" \\
  -d '{
    "task": "Help me register an LLC in Washington state for my tech consulting business",
    "user_id": "user123",
    "priority": 1
  }'
            </pre>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    # Check MCP manager status
    mcp_status = mcp_manager.get_server_status()

    # Check agent status
    agent_status = {name: agent.get_status() for name, agent in agents.items()}

    # Overall health
    all_mcp_connected = all(
        status.get("connected", False)
        for status in mcp_status.values()
    )

    all_agents_active = all(
        agent_info.get("is_active", False)
        for agent_info in agent_status.values()
    )

    overall_status = "healthy" if (all_mcp_connected and all_agents_active) else "degraded"

    return {
        "status": overall_status,
        "service": "yogabrata-ai-platform",
        "version": "2.0.0",
        "mcp_connections": mcp_status,
        "active_agents": list(agents.keys()),
        "agent_status": agent_status,
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/api/v2/mcp/status")
async def get_mcp_status():
    """Get detailed MCP server status"""
    return {
        "mcp_manager": {
            "total_servers": len(mcp_manager.connections),
            "server_status": mcp_manager.get_server_status()
        }
    }

@app.get("/api/v2/agents")
async def list_agents():
    """List all available AI agents"""
    return {
        "agents": [
            {
                "name": agent.name,
                "description": agent.description,
                "capabilities": agent.capabilities,
                "is_active": agent.is_active,
                "required_mcp_servers": agent.get_required_mcp_servers()
            }
            for agent in agents.values()
        ]
    }

@app.get("/api/v2/agents/{agent_name}")
async def get_agent_info(agent_name: str):
    """Get information about a specific agent"""
    if agent_name not in agents:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    agent = agents[agent_name]
    return agent.get_status()

@app.post("/api/v2/agents/{agent_name}/execute")
async def execute_agent_task(
    agent_name: str,
    request: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Execute a task using a specific AI agent"""

    if agent_name not in agents:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    # Extract task information
    task = request.get("task", "")
    if not task:
        raise HTTPException(status_code=400, detail="Task description is required")

    user_id = request.get("user_id", "anonymous")
    priority = request.get("priority", 1)
    metadata = request.get("metadata", {})

    # Create task context
    context = TaskContext(
        user_id=user_id,
        task_id=f"task_{asyncio.get_event_loop().time()}",
        priority=priority,
        metadata=metadata
    )

    # Execute task
    agent = agents[agent_name]

    try:
        response = await agent.execute_task(task, context)
        return {
            "success": response.success,
            "message": response.message,
            "data": response.data,
            "agent_name": response.agent_name,
            "execution_time": response.execution_time,
            "mcp_sources": response.mcp_sources,
            "timestamp": response.timestamp.isoformat()
        }
    except Exception as e:
        logger.error(f"Task execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")

# Startup Formation Workflow Endpoints
@app.post("/api/v2/startup/create")
async def create_startup_workflow(request: Dict[str, Any]):
    """Create a new startup formation workflow"""
    if "startup_orchestrator" not in agents:
        raise HTTPException(status_code=503, detail="Startup Formation Orchestrator not available")

    task = request.get("task", "Create startup workflow")
    user_id = request.get("user_id", "anonymous")

    context = TaskContext(
        user_id=user_id,
        task_id=f"startup_{asyncio.get_event_loop().time()}",
        priority=1,
        metadata=request
    )

    orchestrator = agents["startup_orchestrator"]
    response = await orchestrator.execute_task(task, context)

    return {
        "success": response.success,
        "message": response.message,
        "data": response.data,
        "execution_time": response.execution_time,
        "timestamp": response.timestamp.isoformat()
    }

@app.get("/api/v2/startup/workflows")
async def list_startup_workflows():
    """List all active startup formation workflows"""
    if "startup_orchestrator" not in agents:
        raise HTTPException(status_code=503, detail="Startup Formation Orchestrator not available")

    orchestrator = agents["startup_orchestrator"]
    workflows = orchestrator.list_active_workflows()

    return {
        "workflows": workflows,
        "total_count": len(workflows),
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/api/v2/startup/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get status of a specific startup formation workflow"""
    if "startup_orchestrator" not in agents:
        raise HTTPException(status_code=503, detail="Startup Formation Orchestrator not available")

    orchestrator = agents["startup_orchestrator"]
    workflow_summary = orchestrator.get_workflow_summary(workflow_id)

    if not workflow_summary:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")

    return {
        "workflow": workflow_summary,
        "timestamp": asyncio.get_event_loop().time()
    }

@app.post("/api/v2/startup/workflows/{workflow_id}/visualization")
async def get_workflow_visualization(workflow_id: str):
    """Get workflow visualization data"""
    if "startup_orchestrator" not in agents:
        raise HTTPException(status_code=503, detail="Startup Formation Orchestrator not available")

    context = TaskContext(
        user_id="visualization_request",
        task_id=f"viz_{workflow_id}",
        priority=1,
        metadata={"workflow_id": workflow_id}
    )

    orchestrator = agents["startup_orchestrator"]
    response = await orchestrator.execute_task("Get workflow visualization", context)

    return {
        "success": response.success,
        "message": response.message,
        "data": response.data,
        "execution_time": response.execution_time,
        "timestamp": response.timestamp.isoformat()
    }

@app.get("/api/v2/startup/templates")
async def get_workflow_templates():
    """Get available workflow templates"""
    if "startup_orchestrator" not in agents:
        raise HTTPException(status_code=503, detail="Startup Formation Orchestrator not available")

    orchestrator = agents["startup_orchestrator"]

    return {
        "templates": {
            "llc": {
                "name": "Limited Liability Company (LLC)",
                "description": "Complete LLC formation workflow for US businesses",
                "estimated_duration": "3-5 business days",
                "steps": len(orchestrator.workflow_templates.get("llc", [])),
                "states_supported": ["Washington", "California", "Texas", "Florida", "New York"]
            },
            "corporation": {
                "name": "Corporation (C-Corp/S-Corp)",
                "description": "Complete corporation formation workflow",
                "estimated_duration": "5-7 business days",
                "steps": len(orchestrator.workflow_templates.get("corporation", [])),
                "states_supported": ["Washington", "Delaware", "California", "Texas"]
            }
        },
        "timestamp": asyncio.get_event_loop().time()
    }

# Legacy endpoints for backward compatibility
@app.get("/api/v1/classes")
async def get_classes():
    """Legacy endpoint - redirect to business formation agent"""
    # Use business formation agent for demo
    if "business_formation" in agents:
        context = TaskContext(user_id="legacy", task_id="legacy_classes")
        response = await agents["business_formation"].execute_task(
            "Provide information about business classes and training",
            context
        )
        return {"classes": response.data, "agent_response": response.message}
    else:
        return {"classes": [], "message": "Business Formation Agent not available"}

@app.get("/api/v1/instructors")
async def get_instructors():
    """Legacy endpoint - redirect to business formation agent"""
    if "business_formation" in agents:
        context = TaskContext(user_id="legacy", task_id="legacy_instructors")
        response = await agents["business_formation"].execute_task(
            "Find business consultants and advisors",
            context
        )
        return {"instructors": response.data, "agent_response": response.message}
    else:
        return {"instructors": [], "message": "Business Formation Agent not available"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
