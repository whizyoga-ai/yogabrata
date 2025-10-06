@echo off
echo 🧘‍♀️ Yogabrata Deployment Script for Windows
echo ==========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "docker-compose.yml" (
    echo ❌ docker-compose.yml not found. Please run this script from the project root.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Create necessary directories
if not exist "infrastructure\ssl" (
    mkdir infrastructure\ssl
    echo 📁 Created infrastructure\ssl directory
)

REM Build and start services
echo 🚀 Building and starting services...
docker-compose up -d --build

if errorlevel 1 (
    echo ❌ Failed to start services
    pause
    exit /b 1
)

echo.
echo ✅ Services started successfully!
echo.

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Health check
echo 🔍 Checking service health...
curl -f http://localhost/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Health check failed, but services may still be starting up.
) else (
    echo ✅ Health check passed
)

echo.
echo 🎉 Deployment complete!
echo 📋 Service URLs:
echo   - Frontend: http://localhost
echo   - Backend API: http://localhost/api
echo   - API Documentation: http://localhost/api/docs
echo   - Health Check: http://localhost/health
echo.

REM Show running containers
echo 📊 Running containers:
docker-compose ps

echo.
echo Press any key to stop services and exit...
pause >nul

REM Stop services
echo 🛑 Stopping services...
docker-compose down

echo ✅ Done!
