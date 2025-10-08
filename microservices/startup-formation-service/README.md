# Startup Formation Service

Independent microservice for handling complete business formation workflows and orchestration.

## Overview

This service manages end-to-end startup formation processes including:
- Business entity formation workflows
- Government integration (WA SOS, DOR, IRS)
- Document generation and management
- Progress tracking and status updates
- Founder verification and management

## Architecture

### Technology Stack
- **Backend**: Python/FastAPI
- **Frontend**: Next.js/React
- **Database**: PostgreSQL
- **AI Orchestration**: n8n.io workflows + custom agents
- **Message Queue**: RabbitMQ
- **Container**: Docker

### Core Components

#### 1. Workflow Orchestrator (`src/orchestrator/`)
- Main workflow engine based on n8n.io patterns
- State management and persistence
- Step execution coordination
- Error handling and retry logic

#### 2. Government Integrations (`src/integrations/`)
- WA Secretary of State API integration
- WA Department of Revenue integration
- IRS EIN application system
- Real-time status checking

#### 3. Document Engine (`src/documents/`)
- Dynamic document generation
- Template management system
- PDF generation and processing
- Digital signature integration

#### 4. Frontend Application (`frontend/`)
- Workflow progress visualization
- Real-time status updates
- Document management interface
- Founder dashboard

## Database Schema

### Core Tables
- `workflows` - Main workflow instances
- `workflow_steps` - Individual steps in workflows
- `founder_profiles` - Founder information and verification
- `company_entities` - Business entity data
- `documents` - Generated document storage
- `integration_logs` - Government API interaction logs

## API Endpoints

### Workflow Management
- `POST /api/v1/workflows` - Create new workflow
- `GET /api/v1/workflows/{id}` - Get workflow status
- `PUT /api/v1/workflows/{id}/steps/{step_id}` - Update step status
- `GET /api/v1/workflows/{id}/visualization` - Get workflow diagram

### Document Management
- `GET /api/v1/documents/{workflow_id}` - List workflow documents
- `POST /api/v1/documents/{workflow_id}/generate` - Generate documents
- `GET /api/v1/documents/{id}/download` - Download document

### Integration Status
- `GET /api/v1/integrations/status` - Get all integration statuses
- `POST /api/v1/integrations/{integration}/retry` - Retry failed integration

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- PostgreSQL 13+

### Local Development
```bash
# Clone and setup
git clone <repository-url>
cd startup-formation-service

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install

# Database setup
docker-compose up postgres -d

# Run migrations
cd backend
alembic upgrade head

# Start services
docker-compose up -d

# Development mode
cd backend && python main.py  # API server
cd frontend && npm run dev    # Frontend dev server
```

## Agentic AI Orchestration

### Workflow Agents
1. **Founder Verification Agent** - Validates founder information
2. **Business Analysis Agent** - Analyzes business requirements
3. **Document Preparation Agent** - Generates legal documents
4. **Government Submission Agent** - Handles API submissions
5. **Compliance Monitoring Agent** - Tracks compliance requirements

### n8n.io Integration
- Visual workflow designer for complex business logic
- Trigger-based automation for government API calls
- Conditional logic for different business entity types
- Integration with external services and APIs

## Deployment

### Docker Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale api=3
```

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis for caching
- `RABBITMQ_URL` - Message queue
- `WA_SOS_API_KEY` - Washington SOS API key
- `IRS_API_CREDENTIALS` - IRS service credentials

## Monitoring

### Health Checks
- `/health` - Service health endpoint
- `/metrics` - Prometheus metrics
- Database connectivity checks
- External API status checks

### Logging
- Structured logging with correlation IDs
- Integration with ELK stack
- Error tracking and alerting
- Performance monitoring

## Security

- JWT-based authentication
- API key management for government services
- Encrypted database connections
- Secure document storage
- Audit logging for compliance

## Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## CI/CD Pipeline

- Automated testing on pull requests
- Security scanning
- Performance testing
- Automated deployment to staging/production
- Database migration automation
