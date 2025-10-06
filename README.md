# Yogabrata.com - Multi-Service AI Platform with MCP Integration

An intelligent web application hosted on yogabrata.com that offers AI-powered services through an agentic workflow with MCP (Model Context Protocol) server integration. The platform provides specialized services through autonomous AI agents that connect to free MCP servers for real-time government, legal, and business data.

## 🎯 Core Service Menu

1. **Launch Start-up** (WA State Compliance Focus)
2. **Content Moderation & Promotions**
3. **Hire & Fire AI Bots / Robots**
4. **Legal Compliance Assistant**
5. **Market Research & Business Intelligence**
6. **Automated Tax & Accounting Setup**
7. **Intellectual Property Protection**
8. **Grant & Funding Finder**

## 🏗️ Technology Stack

- **Frontend:** Next.js 14 with shadcn/ui components
- **Backend:** Python FastAPI with MCP client integration
- **Database:** PostgreSQL with pgVector for AI embeddings
- **AI Framework:** LangChain/LlamaIndex with MCP protocol
- **MCP Servers:** Government and legal data sources integration

## 🧠 Agentic Architecture with MCP Integration

### 1. Orchestrator Agent
Routes tasks and manages MCP server connections intelligently.

### 2. Specialist Agents
Each service has a dedicated AI agent with specific MCP server connections:
- **Business Formation Agent** → WA DOR & SOS servers
- **Legal Compliance Agent** → US Legal & HR Compliance servers
- **IP Protection Agent** → USPTO & Legal servers
- **Funding Agent** → Grants.gov & Market Data servers

### 3. MCP Bridge Manager
Manages connections to external MCP servers for real-time data access.

## 🔗 MCP Server Connections

### Government & Legal Sources
- **Washington State DOR** (`dor.wa.gov`) - Business registration, tax compliance
- **Washington SOS** (`sos.wa.gov`) - Business formation, corporate filings
- **US Legal MCP** - Federal business laws, regulations
- **HR Compliance MCP** - Employment laws, hiring regulations
- **USPTO MCP** - Trademark and patent information
- **Grants.gov MCP** - Federal funding opportunities
- **Market Data MCP** - Industry trends, competitor analysis

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 15+
- Docker (optional)
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/whizyoga-ai/yogabrata.git
   cd yogabrata
   ```

2. **Install dependencies:**
   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd ../backend
   python -m venv venv
   # Windows: venv\Scripts\activate
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy and configure environment files
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

4. **Start services:**
   ```bash
   # Backend (Terminal 1)
   cd backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   python main.py

   # Frontend (Terminal 2)
   cd frontend
   npm run dev
   ```

5. **Access the application:**
   - **Platform:** http://localhost:3000
   - **API:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs

## 📁 Project Structure

```
yogabrata/
├── frontend/              # Next.js 14 + shadcn/ui
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── agents/        # AI agent interfaces
│   │   ├── services/      # Service-specific pages
│   │   └── lib/          # Utilities and configurations
├── backend/              # FastAPI + MCP integration
│   ├── agents/           # AI agent implementations
│   ├── mcp/             # MCP server connections
│   ├── services/        # Business logic for each service
│   └── core/           # Core application logic
├── infrastructure/      # Deployment & configuration
├── docs/               # Documentation
├── .github/           # CI/CD workflows
└── README.md
```

## 🔧 Development Workflow

### Branch Strategy
- `main` - Production branch
- `develop` - Development branch
- `feature/*` - New feature branches
- `mcp/*` - MCP server integration branches

### Key Commands
```bash
# Create MCP integration branch
git checkout -b mcp/washington-dor-integration

# Test MCP connections
cd backend && python -m pytest tests/test_mcp_connections.py -v

# Run agent workflow tests
python -m pytest tests/test_agent_workflows.py -v
```

## 🤖 MCP Integration Setup

### 1. MCP Manager Class
```python
from mcp.client import MCPClient

class MCPManager:
    def __init__(self):
        self.connections = {}

    async def connect_dor_wa_gov(self) -> MCPClient:
        """Connect to Washington State DOR"""
        # Implementation for DOR API connection

    async def connect_sos_wa_gov(self) -> MCPClient:
        """Connect to Washington Secretary of State"""
        # Implementation for SOS API connection
```

### 2. Agent Integration
```python
from agents.business_formation_agent import BusinessFormationAgent

# Initialize agent with MCP connections
agent = BusinessFormationAgent(mcp_manager)
result = await agent.launch_startup(business_info)
```

## 🚢 Deployment

### Production Deployment
```bash
# Using Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Manual deployment
./infrastructure/deploy.sh production
```

### Environment Configuration
- **Development:** `.env.development`
- **Staging:** `.env.staging`
- **Production:** `.env.production`

## 📚 Documentation

- [MCP Integration Guide](./docs/mcp-integration.md)
- [Agent Architecture](./docs/agent-architecture.md)
- [API Documentation](./docs/api.md)
- [Service Implementation](./docs/services.md)

## 🔒 Security & Compliance

- **Data Protection:** All sensitive business data encrypted
- **API Security:** JWT authentication with rate limiting
- **Compliance:** SOC 2 Type II certified infrastructure
- **Privacy:** GDPR and CCPA compliant data handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-mcp-server`)
3. Add MCP server integration with tests
4. Commit your changes (`git commit -m 'Add MCP server integration'`)
5. Push to the branch (`git push origin feature/amazing-mcp-server`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@yogabrata.com or create an issue on GitHub.

---

**Built with 🤖 AI + 🔗 MCP Integration by the Yogabrata Team**
