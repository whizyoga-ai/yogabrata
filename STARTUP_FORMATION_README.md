# 🚀 Agentic AI Startup Formation Platform

## Overview

This project implements a comprehensive **Agentic AI workflow** for automating the end-to-end process of founding and operating a startup in the USA. The system dynamically engages with key federal/state APIs, HR/payroll SaaS, compliance/audit platforms, and provides realistic fallback mocks where live endpoints are unavailable.

## 🌟 Key Features

### 🤖 Multi-Agent Architecture
- **Startup Formation Orchestrator**: Coordinates end-to-end workflow with multi-founder support
- **Business Formation Agent**: Handles entity registration and state compliance
- **Legal Compliance Agent**: Manages regulatory requirements and compliance monitoring
- **Content Strategy Agent**: Provides business intelligence and market research

### 🔄 Dynamic Workflow Management
- **Multi-founder role detection**: Automatically assigns tasks based on founder roles (CEO, CFO, CTO)
- **Dependency tracking**: Smart workflow step sequencing with prerequisite management
- **Progress visualization**: Real-time workflow status with Mermaid diagram generation
- **Error handling**: Comprehensive fallback mechanisms and retry logic

### 🌐 MCP Integration Framework
- **Government APIs**: Secretary of State, IRS EIN, SAM.gov integration
- **Payroll Systems**: ADP, Gusto, Paychex mock integrations
- **Legal Compliance**: US Code, CFR, State statutes access
- **Tax Authorities**: State DOR integration and compliance

### 🎨 Visual Interface
- **Interactive workflow diagrams**: n8n.io-style visual progress tracking
- **Real-time updates**: Live progress monitoring and status updates
- **Template system**: Pre-configured workflows for LLCs and Corporations
- **Multi-state support**: Washington, California, Texas, Florida, New York

## 🏗️ Architecture

### Backend Components

#### 1. Agent Framework (`backend/agents/`)
- **BaseAgent**: Abstract base class for all AI agents
- **StartupFormationOrchestrator**: Main workflow coordinator
- **BusinessFormationAgent**: Entity registration specialist
- **LegalComplianceAgent**: Regulatory compliance expert
- **ContentStrategyAgent**: Market intelligence provider

#### 2. MCP Integration (`backend/core/`)
- **MCPManager**: Manages connections to external data sources
- **MCPMockServers**: Realistic mock implementations for development
- **Database**: Workflow state persistence and history tracking

#### 3. API Layer (`backend/main.py`)
- **FastAPI Backend**: RESTful API with comprehensive endpoints
- **Workflow Management**: Create, monitor, and visualize workflows
- **Agent Execution**: Task processing and response handling

### Frontend Components

#### 1. User Interface (`frontend/src/app/`)
- **Startup Formation Page**: Complete workflow creation and monitoring interface
- **Workflow Visualization**: Interactive Mermaid diagram display
- **Progress Tracking**: Real-time status updates and progress indicators

#### 2. UI Components (`frontend/src/components/`)
- **shadcn/ui Components**: Modern, accessible UI component library
- **Workflow Visualization**: Custom Mermaid diagram renderer
- **Form Components**: Multi-step workflow creation forms

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (optional)

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start Mock Servers** (for development)
   ```bash
   cd backend
   python core/mcp_mock_servers.py
   ```
   Mock servers will run on `http://localhost:8001`

3. **Start Main API Server**
   ```bash
   cd backend
   python main.py
   ```
   API server will run on `http://localhost:8000`

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

## 📋 Usage Guide

### Creating a Startup Workflow

1. **Navigate to Startup Formation**
   - Visit `http://localhost:3000/startup-formation`
   - Or click "Launch Startup Formation Platform" from the main page

2. **Fill in Company Information**
   ```typescript
   {
     companyName: "Your Company LLC",
     entityType: "llc", // or "corporation"
     state: "washington",
     industry: "technology",
     founderName: "John Doe",
     founderEmail: "john@yourcompany.com",
     founderRole: "ceo"
   }
   ```

3. **Submit and Monitor**
   - Click "Create Workflow" to start the automated process
   - Monitor progress in real-time with visual workflow diagrams
   - Receive notifications when steps complete

### API Usage

#### Create Workflow via API
```bash
curl -X POST http://localhost:8000/api/v2/startup/create \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create LLC for Sample Tech in Washington",
    "user_id": "user123",
    "company_info": {
      "name": "Sample Tech LLC",
      "entity_type": "llc",
      "state": "washington",
      "industry": "technology",
      "founders": [{
        "name": "John Doe",
        "email": "john@sampletech.com",
        "role": "ceo",
        "ownership_percentage": 100
      }]
    }
  }'
```

#### Check Workflow Status
```bash
curl http://localhost:8000/api/v2/startup/workflows/wf_20241006_120000
```

#### Get Workflow Visualization
```bash
curl -X POST http://localhost:8000/api/v2/startup/workflows/wf_20241006_120000/visualization
```

## 🔧 Configuration

### Environment Variables

Create `.env` files in both `backend/` and `frontend/` directories:

#### Backend (.env)
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Mock Server Configuration
MOCK_SERVER_URL=http://localhost:8001
USE_MOCK_SERVERS=true

# Database
DATABASE_URL=sqlite:///startup_formation.db

# Logging
LOG_LEVEL=INFO
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MOCK_API_URL=http://localhost:8001
```

### Workflow Templates

The system includes pre-configured templates for:

#### LLC Formation (10 steps)
1. Analyze Business Requirements
2. Check Name Availability
3. Prepare Articles of Organization
4. File State Registration
5. Obtain EIN
6. Setup Business Banking
7. Register State Taxes
8. Setup Payroll System
9. Setup Compliance Monitoring
10. Generate Operating Agreement

#### Corporation Formation (8 steps)
1. Analyze Corporate Requirements
2. Check Name Availability
3. Prepare Articles of Incorporation
4. File State Registration
5. Obtain EIN
6. Setup Business Banking
7. Register State Taxes
8. Setup Compliance Monitoring

## 🔍 Workflow Steps Details

### Step 1: Analyze Business Requirements
- **Duration**: 15 minutes
- **MCP Sources**: WA SOS, Legal Compliance
- **Output**: Recommended business structure and requirements

### Step 2: Check Name Availability
- **Duration**: 10 minutes
- **MCP Sources**: WA SOS
- **Output**: Name availability status and alternatives

### Step 3: Prepare Articles of Organization
- **Duration**: 20 minutes
- **MCP Sources**: Legal templates
- **Output**: Completed Articles document

### Step 4: File State Registration
- **Duration**: 30 minutes
- **MCP Sources**: WA SOS API
- **Output**: Registration number and filing confirmation

### Step 5: Obtain EIN
- **Duration**: 25 minutes
- **MCP Sources**: IRS EIN API
- **Output**: Employer Identification Number

### Step 6: Setup Business Banking
- **Duration**: 45 minutes
- **MCP Sources**: Banking recommendations
- **Output**: Banking setup guidance

### Step 7: Register State Taxes
- **Duration**: 20 minutes
- **MCP Sources**: WA DOR
- **Output**: Tax registration numbers and filing schedule

### Step 8: Setup Payroll System
- **Duration**: 35 minutes
- **MCP Sources**: ADP, Gusto, Paychex APIs
- **Output**: Payroll system configuration

### Step 9: Setup Compliance Monitoring
- **Duration**: 30 minutes
- **MCP Sources**: Legal compliance data
- **Output**: Compliance monitoring setup

### Step 10: Generate Operating Agreement
- **Duration**: 40 minutes
- **MCP Sources**: Legal templates
- **Output**: Customized operating agreement

## 📊 Monitoring and Analytics

### Workflow Metrics
- **Progress Tracking**: Real-time percentage completion
- **Time Tracking**: Actual vs. estimated duration
- **Step Status**: Pending, In Progress, Completed, Failed
- **Error Rates**: Failed step analysis and retry tracking

### Visual Analytics
- **Mermaid Diagrams**: Interactive workflow flowcharts
- **Progress Bars**: Visual completion indicators
- **Status Badges**: Color-coded step status
- **Timeline Views**: Gantt-style progress visualization

## 🔒 Security and Compliance

### Data Protection
- **PII Handling**: Secure storage of personal information
- **API Security**: JWT-based authentication for external APIs
- **Audit Logging**: Comprehensive activity tracking

### Compliance Features
- **GDPR Ready**: Data protection compliance
- **SOX Compliance**: Financial reporting standards
- **State Regulations**: Multi-state legal compliance
- **Tax Compliance**: Automated filing reminders

## 🧪 Testing

### Mock Server Testing
All external APIs have mock implementations for testing:

```bash
# Start mock servers
cd backend
python core/mcp_mock_servers.py

# Run tests
python -m pytest tests/
```

### Integration Testing
```bash
# Test complete workflow
curl -X POST http://localhost:8000/api/v2/startup/create \
  -H "Content-Type: application/json" \
  -d @test-workflow.json
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individually
docker build -f backend/Dockerfile -t startup-backend .
docker build -f frontend/Dockerfile -t startup-frontend .
```

### Production Deployment
```bash
# Use production environment variables
export USE_MOCK_SERVERS=false
export NODE_ENV=production

# Deploy with real API keys
export IRS_API_KEY=your_irs_key
export ADP_CLIENT_ID=your_adp_id
```

## 📚 Documentation

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **Mock Endpoints**: See `docs/mock_endpoints_documentation.md`
- **Integration Guide**: See `docs/integration_guide.md`

### Code Documentation
- **Backend**: Comprehensive docstrings in all modules
- **Frontend**: TypeScript interfaces and JSDoc comments
- **Architecture**: System design documents in `docs/`

## 🤝 Contributing

### Development Workflow
1. Create feature branch from `main`
2. Implement changes with tests
3. Update documentation
4. Submit pull request

### Code Standards
- **Backend**: PEP 8, type hints, comprehensive testing
- **Frontend**: TypeScript, ESLint, component testing
- **Documentation**: Clear examples and API references

## 📞 Support

### Getting Help
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and ideas
- **Documentation**: Comprehensive guides and API references

### Troubleshooting
- **Mock Servers**: Check `http://localhost:8001/mock-admin/stats`
- **API Status**: Visit `http://localhost:8000/health`
- **Logs**: Check application logs for detailed error information

## 🔄 Future Enhancements

### Planned Features
- [ ] **Multi-language support**: Spanish, French, German interfaces
- [ ] **Advanced analytics**: Machine learning insights and predictions
- [ ] **Mobile app**: iOS and Android native applications
- [ ] **API marketplace**: Third-party integrations and extensions
- [ ] **Advanced compliance**: International business formation
- [ ] **AI-powered optimization**: Automated workflow improvements

### Integration Roadmap
- [ ] **Real government APIs**: Live Secretary of State integrations
- [ ] **Banking APIs**: Direct bank account setup and management
- [ ] **Tax filing**: Automated quarterly and annual tax filing
- [ ] **Legal document generation**: AI-powered contract creation
- [ ] **Insurance integration**: Business insurance setup and management

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI**: For providing the foundation AI models
- **LangChain**: For the orchestration framework
- **FastAPI**: For the robust API backend
- **Next.js**: For the modern React framework
- **shadcn/ui**: For the beautiful UI components
- **Mermaid**: For the workflow visualization

---

**Built with ❤️ for entrepreneurs and startup founders**
