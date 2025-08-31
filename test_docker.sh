#!/bin/bash
set -e

echo "🧪 Testing Docker Setup for Social Image Generator"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_status "error" "Docker is not installed"
    exit 1
fi

print_status "success" "Docker is available"

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    print_status "error" "docker-compose is not available"
    exit 1
fi

print_status "success" "Docker Compose is available ($DOCKER_COMPOSE_CMD)"

# Clean up any existing containers
print_status "info" "Cleaning up existing containers..."
$DOCKER_COMPOSE_CMD down --remove-orphans 2>/dev/null || true
docker rm -f social-image-generator social-image-generator-dev social-image-generator-test 2>/dev/null || true

# Build the Docker image
print_status "info" "Building Docker image..."
if $DOCKER_COMPOSE_CMD build; then
    print_status "success" "Docker image built successfully"
else
    print_status "error" "Failed to build Docker image"
    exit 1
fi

# Start the container
print_status "info" "Starting Docker container..."
if $DOCKER_COMPOSE_CMD up -d; then
    print_status "success" "Docker container started"
else
    print_status "error" "Failed to start Docker container"
    exit 1
fi

# Wait for container to be healthy
print_status "info" "Waiting for container to be healthy..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker ps | grep -q "social-image-generator" && docker inspect social-image-generator | grep -q '"Status": "healthy"'; then
        print_status "success" "Container is healthy"
        break
    fi

    echo "   Attempt $attempt/$max_attempts: Waiting for container to be healthy..."
    sleep 5
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_status "warning" "Container health check timed out, but continuing..."
fi

# Test the API endpoints
print_status "info" "Testing API endpoints..."

# Test health endpoint
if curl -s -f http://localhost:5000/health > /dev/null 2>&1; then
    print_status "success" "Health endpoint is responding"
else
    print_status "error" "Health endpoint is not responding"
fi

# Test gradient info endpoint
if curl -s -f http://localhost:5000/gradient_info > /dev/null 2>&1; then
    print_status "success" "Gradient info endpoint is working"
else
    print_status "warning" "Gradient info endpoint is not responding"
fi

# Test gradient generation
print_status "info" "Testing gradient generation..."
test_response=$(curl -s -X POST http://localhost:5000/generate_gradient \
    -H "Content-Type: application/json" \
    -d '{
        "width": 1080,
        "height": 1350,
        "colors": ["#FF6B6B", "#FFD93D", "#6BCB77"],
        "gradient_type": "linear",
        "direction": "vertical",
        "use_hsl_interpolation": true
    }' 2>/dev/null)

if echo "$test_response" | grep -q '"success": true'; then
    print_status "success" "Gradient generation is working"
    # Extract filename from response
    filename=$(echo "$test_response" | grep -o '"filename": "[^"]*"' | cut -d'"' -f4)
    if [ -n "$filename" ]; then
        print_status "success" "Generated file: $filename"
    fi
else
    print_status "error" "Gradient generation failed"
    echo "Response: $test_response"
fi

# Check if files are being created in the correct directories
print_status "info" "Checking volume mounts..."

# Check if generated directory has files
if [ -d "./generated" ] && [ "$(ls -A ./generated 2>/dev/null)" ]; then
    file_count=$(ls ./generated | wc -l)
    print_status "success" "Generated directory has $file_count files"
else
    print_status "warning" "Generated directory is empty or doesn't exist"
fi

# Check if uploads directory exists
if [ -d "./uploads" ]; then
    print_status "success" "Uploads directory is mounted correctly"
else
    print_status "error" "Uploads directory is not mounted"
fi

# Show container logs
print_status "info" "Container logs:"
$DOCKER_COMPOSE_CMD logs --tail=20

# Summary
echo ""
print_status "info" "Docker test completed!"
echo ""
echo "📋 Test Summary:"
echo "   - Container: $(docker ps | grep -c social-image-generator || echo 0) running"
echo "   - Health Check: $(curl -s http://localhost:5000/health | grep -c '"status"' || echo 0) working"
echo "   - Generated Files: $(find ./generated -name "*.png" 2>/dev/null | wc -l || echo 0)"
echo ""
echo "🔧 To stop the container: $DOCKER_COMPOSE_CMD down"
echo "🔧 To view logs: $DOCKER_COMPOSE_CMD logs -f"
echo "🔧 To restart: $DOCKER_COMPOSE_CMD restart"
