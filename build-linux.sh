#!/bin/bash
# Linux Build Script for Social Image Generator
# This script handles Linux-specific Docker build requirements

set -e

echo "🐧 Linux Docker Build for Social Image Generator"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "success" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "warning" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    elif [ "$status" = "error" ]; then
        echo -e "${RED}❌ $message${NC}"
    else
        echo -e "${BLUE}ℹ️  $message${NC}"
    fi
}

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_status "warning" "This script is designed for Linux systems"
    print_status "info" "For Windows, use: .\test_docker.ps1"
fi

# Check Docker and Docker Compose
if ! command -v docker &> /dev/null; then
    print_status "error" "Docker is not installed"
    echo "Install Docker: https://docs.docker.com/engine/install/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_status "error" "Docker Compose is not available"
    echo "Install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

print_status "success" "Docker and Docker Compose are available"

# Create required directories with proper permissions
print_status "info" "Creating required directories..."
mkdir -p uploads/main uploads/watermark uploads/background generated output config

# Set proper permissions for volume mounts
chmod -R 755 uploads generated output
print_status "success" "Directories created and permissions set"

# Clean up existing containers
print_status "info" "Cleaning up existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true
docker rm -f $(docker ps -aq --filter "name=social-image-generator") 2>/dev/null || true
print_status "success" "Cleanup completed"

# Check available ports
print_status "info" "Checking port availability..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_status "warning" "Port 5000 is in use, will try alternative ports"
    export PORT=5001
else
    print_status "success" "Port 5000 is available"
fi

# Build and run with Linux-specific configuration
print_status "info" "Building and starting container..."

if [ -f "docker-compose.linux.yml" ]; then
    print_status "info" "Using Linux-specific configuration"
    docker-compose -f docker-compose.yml -f docker-compose.linux.yml up --build -d
else
    print_status "warning" "Linux config not found, using standard config"
    docker-compose up --build -d
fi

# Wait for container to start
print_status "info" "Waiting for container to start..."
sleep 10

# Check if container is running
if docker-compose ps | grep -q "social-image-generator"; then
    print_status "success" "Container is running!"
else
    print_status "error" "Container failed to start"
    echo "Check logs: docker-compose logs"
    exit 1
fi

# Test the API
print_status "info" "Testing API endpoints..."

# Get the actual port being used
ACTUAL_PORT=$(docker-compose ps | grep -o ":[0-9]*->5000" | cut -d':' -f2 | head -1)
if [ -z "$ACTUAL_PORT" ]; then
    ACTUAL_PORT=5000
fi

echo "API should be available at: http://localhost:$ACTUAL_PORT"

# Test health endpoint
if curl -s -f "http://localhost:$ACTUAL_PORT/health" >/dev/null 2>&1; then
    print_status "success" "Health endpoint is responding"
else
    print_status "warning" "Health endpoint not responding yet, container may still be starting"
fi

echo ""
print_status "success" "Build completed successfully!"
echo ""
echo "📋 Management Commands:"
echo "   Stop: docker-compose down"
echo "   Logs: docker-compose logs -f"
echo "   Restart: docker-compose restart"
echo "   Rebuild: docker-compose up --build --force-recreate -d"
echo ""
echo "🌐 API Endpoints:"
echo "   Health: http://localhost:$ACTUAL_PORT/health"
echo "   Main API: http://localhost:$ACTUAL_PORT/"
echo "   Gradient Generator: http://localhost:$ACTUAL_PORT/generate_gradient"
