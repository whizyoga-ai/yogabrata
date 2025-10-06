from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(
    title="Yogabrata API",
    description="API for Yogabrata wellness platform",
    version="1.0.0",
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
        <title>Yogabrata API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧘‍♀️ Yogabrata API</h1>
            <p>Welcome to the Yogabrata wellness platform API!</p>

            <h2>Available Endpoints:</h2>
            <div class="endpoint">
                <strong>GET /</strong> - This information page
            </div>
            <div class="endpoint">
                <strong>GET /docs</strong> - Interactive API documentation (Swagger UI)
            </div>
            <div class="endpoint">
                <strong>GET /redoc</strong> - Alternative API documentation (ReDoc)
            </div>
            <div class="endpoint">
                <strong>GET /health</strong> - Health check endpoint
            </div>

            <h2>Quick Start:</h2>
            <p>Visit <a href="/docs">/docs</a> for interactive API documentation</p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "yogabrata-api",
        "version": "1.0.0"
    }

@app.get("/api/v1/classes")
async def get_classes():
    """Get all yoga classes"""
    return {
        "classes": [
            {
                "id": 1,
                "name": "Hatha Yoga",
                "instructor": "Sarah Johnson",
                "duration": 60,
                "capacity": 20
            },
            {
                "id": 2,
                "name": "Vinyasa Flow",
                "instructor": "Mike Chen",
                "duration": 75,
                "capacity": 15
            }
        ]
    }

@app.get("/api/v1/instructors")
async def get_instructors():
    """Get all instructors"""
    return {
        "instructors": [
            {
                "id": 1,
                "name": "Sarah Johnson",
                "specialties": ["Hatha", "Meditation"],
                "experience_years": 8
            },
            {
                "id": 2,
                "name": "Mike Chen",
                "specialties": ["Vinyasa", "Power Yoga"],
                "experience_years": 12
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
