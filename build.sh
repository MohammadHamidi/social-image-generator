#!/bin/bash

# Build script for Social Image Generator Docker image
# This script reads configuration from .env file and builds the Docker image

set -e  # Exit on error

echo "=========================================="
echo "Social Image Generator - Docker Build"
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

echo "Building Docker image..."
echo "Image name: ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""

# Build the Docker image
docker build \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    -f Dockerfile \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Build completed successfully!"
    echo "=========================================="
    echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    echo ""
    echo "To run the container, execute: ./run.sh"
else
    echo ""
    echo "=========================================="
    echo "❌ Build failed!"
    echo "=========================================="
    exit 1
fi
