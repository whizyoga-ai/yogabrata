#!/bin/bash

# 🚀 Startup Formation Platform Runner
# This script starts all components of the Agentic AI Startup Formation Platform

echo "🚀 Starting Yogabrata AI Startup Formation Platform..."
echo "=================================================="

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo "Killing process on port $port..."
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        kill -9 $pid
        sleep 2
    fi
}

# Clean up any existing processes
echo "🧹 Cleaning up existing processes..."
kill_port 8000
kill_port 8001
kill_port 3000

# Start Mock MCP Servers (Port 8001)
echo "📡 Starting MCP Mock Servers on port 8001..."
cd backend
python core/mcp_mock_servers.py &
MOCK_PID=$!
cd ..

echo "✅ Mock servers starting (PID: $MOCK_PID)"
sleep 3

# Start Main Backend API (Port 8000)
echo "🔧 Starting Backend API on port 8000..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

echo "✅ Backend API starting (PID: $BACKEND_PID)"
sleep 5

# Check if servers are running
echo "🔍 Checking server status..."

# Check mock server
if curl -s http://localhost:8001/mock-admin/stats > /dev/null; then
    echo "✅ Mock servers are running"
else
    echo "❌ Mock servers failed to start"
fi

# Check backend API
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API failed to start"
fi

echo ""
echo "🎉 Startup Formation Platform is ready!"
echo "======================================"
echo "📋 Available URLs:"
echo "   • Frontend (when running): http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • Mock Server Admin: http://localhost:8001/mock-admin/stats"
echo ""
echo "🚀 Key Features:"
echo "   • Create startup workflows via web interface"
echo "   • Monitor progress with visual diagrams"
echo "   • Test with realistic mock APIs"
echo "   • Multi-founder role support"
echo ""
echo "📝 Quick Test:"
echo "   curl -X POST http://localhost:8000/api/v2/startup/create \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"task\": \"Create LLC for Test Company\", \"user_id\": \"test\"}'"
echo ""
echo "🛑 To stop all servers:"
echo "   kill $MOCK_PID $BACKEND_PID"
echo ""
echo "Happy coding! 🚀"

# Wait for background processes
wait
