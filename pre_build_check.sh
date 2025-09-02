#!/bin/bash
set -e

echo "🔍 Pre-Build Check for Social Image Generator Docker Container"
echo "=============================================================="

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
        return 1
    else
        echo -e "${BLUE}ℹ️  $message${NC}"
    fi
}

# Check if Docker is installed and running
print_status "info" "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_status "error" "Docker is not installed"
    echo "💡 Install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi
print_status "success" "Docker is installed"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    print_status "error" "Docker daemon is not running"
    echo "💡 Start Docker Desktop and try again"
    exit 1
fi
print_status "success" "Docker daemon is running"

# Check Docker version
DOCKER_VERSION=$(docker --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
print_status "info" "Docker version: $DOCKER_VERSION"

# Check required files
print_status "info" "Checking required files..."

REQUIRED_FILES=(
    "Dockerfile"
    "requirements.txt"
    "social_image_api.py"
    "src/enhanced_social_generator.py"
    "docker-compose.yml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_status "error" "Required file missing: $file"
        exit 1
    fi
done
print_status "success" "All required files present"

# Check directory structure
print_status "info" "Checking directory structure..."

REQUIRED_DIRS=(
    "assets/fonts"
    "uploads/main"
    "uploads/watermark"
    "uploads/background"
    "generated"
    "output"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        print_status "warning" "Directory missing: $dir - creating it..."
        mkdir -p "$dir"
        if [ $? -eq 0 ]; then
            print_status "success" "Created directory: $dir"
        else
            print_status "error" "Failed to create directory: $dir"
            exit 1
        fi
    else
        print_status "success" "Directory exists: $dir"
    fi
done

# Check font files
print_status "info" "Checking font files..."
FONT_FILES=(
    "assets/fonts/IRANYekanBoldFaNum.ttf"
    "assets/fonts/IRANYekanMediumFaNum.ttf"
    "assets/fonts/IRANYekanRegularFaNum.ttf"
    "assets/fonts/NotoSans-Bold.ttf"
    "assets/fonts/NotoSans-Regular.ttf"
    "assets/fonts/NotoSansArabic-Bold.ttf"
    "assets/fonts/NotoSansArabic-Regular.ttf"
)

FONT_MISSING=0
for font in "${FONT_FILES[@]}"; do
    if [ ! -f "$font" ]; then
        print_status "warning" "Font file missing: $font"
        FONT_MISSING=$((FONT_MISSING + 1))
    fi
done

if [ $FONT_MISSING -eq 0 ]; then
    print_status "success" "All font files present"
else
    print_status "warning" "$FONT_MISSING font files missing - text rendering may be limited"
fi

# Check Python syntax
print_status "info" "Checking Python syntax..."
PYTHON_FILES=(
    "social_image_api.py"
    "src/enhanced_social_generator.py"
)

for pyfile in "${PYTHON_FILES[@]}"; do
    if python -m py_compile "$pyfile" 2>/dev/null; then
        print_status "success" "Python syntax OK: $pyfile"
    else
        print_status "error" "Python syntax error in: $pyfile"
        exit 1
    fi
done

# Check if ports are available
print_status "info" "Checking if port 5000 is available..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_status "warning" "Port 5000 is already in use"
    echo "💡 The Docker container may fail to start if port 5000 is not available"
else
    print_status "success" "Port 5000 is available"
fi

# Check disk space
print_status "info" "Checking available disk space..."
DISK_SPACE=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$DISK_SPACE" -lt 5 ]; then
    print_status "warning" "Low disk space: ${DISK_SPACE}GB available"
    echo "💡 Docker build requires at least 5GB free space"
else
    print_status "success" "Sufficient disk space: ${DISK_SPACE}GB available"
fi

# Check memory
print_status "info" "Checking available memory..."
MEM_GB=$(free -g | grep '^Mem:' | awk '{print $7}')
if [ "$MEM_GB" -lt 2 ]; then
    print_status "warning" "Low memory: ${MEM_GB}GB available"
    echo "💡 Docker build and container may require more memory"
else
    print_status "success" "Sufficient memory: ${MEM_GB}GB available"
fi

# Clean up old containers/images if any
print_status "info" "Cleaning up old Docker resources..."
docker rm -f social-image-generator social-image-generator-dev social-image-generator-test 2>/dev/null || true
docker rmi -f social-image-generator:latest 2>/dev/null || true
print_status "success" "Cleanup completed"

# Final status
echo ""
print_status "success" "Pre-build check completed successfully!"
echo ""
echo "🚀 Ready to build Docker container"
echo "   Run: docker-compose build"
echo ""
echo "📋 Build command:"
echo "   docker-compose build --no-cache  # Force fresh build"
echo ""
echo "🔧 Alternative commands:"
echo "   ./test_docker.sh                 # Build and test automatically"
echo "   docker build -t social-image-generator .  # Direct Docker build"
echo ""

exit 0
