# Yogabrata Site Microservices

This directory contains independent microservices that were extracted from the monolithic yogabrata-site application.

## Microservices Architecture

Each microservice is completely independent with its own:
- Database (PostgreSQL/MongoDB)
- UI (React/Next.js frontend)
- Core application logic (Python/Node.js backend)
- Agentic AI orchestration (n8n.io workflow patterns)
- Docker containerization
- CI/CD pipeline

## Services

### 1. Startup Formation Service (`startup-formation-service/`)
**Purpose**: Complete business formation workflows and orchestration
- Handles end-to-end startup formation processes
- Government integration (WA SOS, DOR, IRS)
- Workflow orchestration and progress tracking
- Document generation and management

### 2. Legal Compliance Service (`legal-compliance-service/`)
**Purpose**: Legal compliance monitoring and regulatory guidance
- Compliance audits and monitoring
- Legal research and risk assessment
- Regulatory guidance and requirements
- Compliance reporting and documentation

### 3. Content Strategy Service (`content-strategy-service/`)
**Purpose**: Content creation and social media management
- AI-powered content generation
- Social media optimization
- Content moderation and strategy
- Multi-platform content distribution

### 4. Business Formation Service (`business-formation-service/`)
**Purpose**: Core business registration and entity management
- Business entity registration
- License and permit management
- Tax setup and compliance
- Business structure recommendations

### 5. API Gateway Service (`api-gateway-service/`)
**Purpose**: Centralized routing, authentication, and service coordination
- Request routing to appropriate services
- Authentication and authorization
- Rate limiting and security
- Service discovery and load balancing

## Communication Pattern

Services communicate through:
- RESTful APIs
- Message queues (RabbitMQ/Redis)
- Event-driven architecture
- Service mesh (Istio/Linkerd)

## Development Setup

Each service can be developed independently:

```bash
# Navigate to specific service
cd microservices/startup-formation-service

# Install dependencies
npm install  # for Node.js services
pip install -r requirements.txt  # for Python services

# Start service
npm run dev  # development mode
docker-compose up  # containerized
```

## Deployment

Each service is deployed as an independent container/application with:
- Individual scaling capabilities
- Independent release cycles
- Service-specific monitoring
- Isolated failure domains

## Data Management

Each service maintains its own database:
- **Startup Formation**: PostgreSQL with workflow states
- **Legal Compliance**: MongoDB for document storage
- **Content Strategy**: PostgreSQL with content metadata
- **Business Formation**: PostgreSQL with entity data
- **API Gateway**: Redis for caching and session management

## Monitoring and Observability

- Individual health checks per service
- Distributed tracing (Jaeger)
- Centralized logging (ELK stack)
- Metrics collection (Prometheus/Grafana)
