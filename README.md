# Yogabrata.com

A modern full-stack web application built with Next.js, FastAPI, and Nginx.

## 🏗️ Project Structure

```
yogabrata/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── infrastructure/    # Nginx config, Windows scripts
├── docs/             # Documentation
├── .github/          # GitHub Actions workflows
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker (optional)
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/whizyoga-ai/yogabrata.git
   cd yogabrata
   ```

2. **Start the development environment:**
   ```bash
   # Frontend (Next.js)
   cd frontend
   npm install
   npm run dev

   # Backend (FastAPI) - in another terminal
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📁 Project Components

### Frontend (`/frontend`)
- **Framework:** Next.js 14+ with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** React Query / Zustand
- **Features:** Server-side rendering, static generation

### Backend (`/backend`)
- **Framework:** FastAPI
- **Language:** Python 3.9+
- **Database:** PostgreSQL / SQLite
- **Authentication:** JWT tokens
- **API Documentation:** Auto-generated with Swagger UI

### Infrastructure (`/infrastructure`)
- **Web Server:** Nginx
- **Configuration:** Production-ready setup
- **Scripts:** Windows deployment scripts
- **Docker:** Containerization setup

## 🔧 Development Workflow

### Branch Strategy
- `main` - Production branch
- `develop` - Development branch
- `feature/*` - Feature branches
- `hotfix/*` - Hotfix branches

### Git Commands
```bash
# Create a feature branch
git checkout -b feature/new-feature

# Push feature branch
git push -u origin feature/new-feature

# Create pull request on GitHub
# Merge back to develop when ready
```

## 🚢 Deployment

### Production Deployment
1. Merge `develop` → `main`
2. Pull latest changes: `git pull origin main`
3. Run deployment script: `./infrastructure/deploy.sh`

### Docker Deployment (Optional)
```bash
docker-compose up -d
```

## 📚 Documentation

- [API Documentation](./docs/api.md)
- [Frontend Guide](./docs/frontend.md)
- [Backend Guide](./docs/backend.md)
- [Deployment Guide](./docs/deployment.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@yogabrata.com or create an issue on GitHub.

---

**Built with ❤️ by the Yogabrata Team**
