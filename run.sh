#!/bin/bash

# Run script for Social Image Generator Docker container
# This script reads configuration from .env file and runs the Docker container

set -e  # Exit on error

echo "=========================================="
echo "Social Image Generator - Docker Run"
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create a .env file (you can copy from env.example)"
    exit 1
fi

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Set default values if not specified in .env
IMAGE_NAME=${IMAGE_NAME:-social-image-generator}
IMAGE_TAG=${IMAGE_TAG:-latest}
CONTAINER_NAME=${CONTAINER_NAME:-social-image-generator}
PORT=${PORT:-5000}
RESTART_POLICY=${RESTART_POLICY:-unless-stopped}
UPLOADS_DIR=${UPLOADS_DIR:-./uploads}
OUTPUT_DIR=${OUTPUT_DIR:-./output}
GENERATED_DIR=${GENERATED_DIR:-./generated}
CONFIG_DIR=${CONFIG_DIR:-./config}

echo "Container configuration:"
echo "  Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "  Container name: ${CONTAINER_NAME}"
echo "  Port: ${PORT}"
echo "  Restart policy: ${RESTART_POLICY}"
echo ""

# Create necessary directories if they don't exist
echo "Creating necessary directories..."
mkdir -p "${UPLOADS_DIR}/main" "${UPLOADS_DIR}/background" "${UPLOADS_DIR}/watermark"
mkdir -p "${OUTPUT_DIR}"
mkdir -p "${GENERATED_DIR}"
mkdir -p "${CONFIG_DIR}"

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "Stopping and removing existing container..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

echo "Starting container..."

# Build the docker run command
DOCKER_CMD="docker run -d \
    --name ${CONTAINER_NAME} \
    --restart ${RESTART_POLICY} \
    -p ${PORT}:5000 \
    -v $(pwd)/${UPLOADS_DIR}:/app/uploads \
    -v $(pwd)/${OUTPUT_DIR}:/app/output \
    -v $(pwd)/${GENERATED_DIR}:/app/generated \
    -e FLASK_ENV=${FLASK_ENV:-production} \
    -e PYTHONPATH=/app/src \
    -e PYTHONDONTWRITEBYTECODE=1 \
    -e PORT=5000"

# Add optional memory limit if specified
if [ ! -z "${MEMORY_LIMIT}" ]; then
    DOCKER_CMD="${DOCKER_CMD} --memory ${MEMORY_LIMIT}"
fi

# Add optional CPU limit if specified
if [ ! -z "${CPU_LIMIT}" ]; then
    DOCKER_CMD="${DOCKER_CMD} --cpus ${CPU_LIMIT}"
fi

# Complete the command with the image name
DOCKER_CMD="${DOCKER_CMD} ${IMAGE_NAME}:${IMAGE_TAG}"

# Execute the docker run command
eval $DOCKER_CMD

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Container started successfully!"
    echo "=========================================="
    echo "Container name: ${CONTAINER_NAME}"
    echo "API available at: http://localhost:${PORT}"
    echo ""
    echo "Useful commands:"
    echo "  View logs:        docker logs -f ${CONTAINER_NAME}"
    echo "  Stop container:   docker stop ${CONTAINER_NAME}"
    echo "  Start container:  docker start ${CONTAINER_NAME}"
    echo "  Remove container: docker rm -f ${CONTAINER_NAME}"
    echo ""
    echo "Checking container status..."
    sleep 2
    docker ps -f name=${CONTAINER_NAME} --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    echo ""
    echo "=========================================="
    echo "❌ Failed to start container!"
    echo "=========================================="
    exit 1
fi
