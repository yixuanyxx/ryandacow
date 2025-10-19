#!/bin/bash

# PSA Workforce AI MVP - Start and Test Script
echo "🚀 Starting PSA Workforce AI MVP Services"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "user-management" ] || [ ! -d "recommendations" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo "🔍 Checking services..."

# Function to start a service
start_service() {
    local service_name=$1
    local port=$2
    local dir=$3
    
    echo "🔄 Starting $service_name on port $port..."
    cd "$dir"
    
    # Check if port is already in use
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        echo "⚠️  Port $port is already in use. Killing existing process..."
        lsof -ti:$port | xargs kill -9
        sleep 2
    fi
    
    # Start the service in background
    python3 app.py &
    local pid=$!
    echo "✅ $service_name started with PID: $pid"
    
    # Wait a bit for the service to start
    sleep 3
    
    # Check if service is running
    if curl -s http://localhost:$port/health > /dev/null; then
        echo "✅ $service_name is responding on port $port"
    else
        echo "❌ $service_name failed to start on port $port"
        return 1
    fi
    
    cd ..
    return 0
}

# Start services
echo "🚀 Starting all services..."

start_service "User Management" 5001 "user-management"
if [ $? -ne 0 ]; then
    echo "❌ Failed to start User Management service"
    exit 1
fi

start_service "Recommendations" 5004 "recommendations"
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Recommendations service"
    exit 1
fi

echo ""
echo "🎉 All services started successfully!"
echo ""
echo "📋 Service URLs:"
echo "   - User Management: http://localhost:5001"
echo "   - Recommendations: http://localhost:5004"
echo ""
echo "🧪 Running endpoint tests..."
echo ""

# Run the test script
python3 test_endpoints.py

echo ""
echo "🔍 To test manually, you can use:"
echo "   curl http://localhost:5001/auth/login -X POST -H 'Content-Type: application/json' -d '{\"email\":\"samantha.lee@globalpsa.com\",\"password\":\"demo123\"}'"
echo "   curl http://localhost:5001/users/EMP-20001"
echo "   curl http://localhost:5004/recommendations/EMP-20001"
echo ""
echo "🛑 To stop all services, press Ctrl+C or run:"
echo "   pkill -f 'python3 app.py'"
