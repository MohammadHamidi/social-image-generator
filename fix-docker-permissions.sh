#!/bin/bash
# Fix Docker permissions for social-image-generator

echo "🔧 Fixing Docker permissions for social-image-generator..."
echo "==================================================="

# Get container name
CONTAINER_NAME="social-image-generator"

# Method 1: Try fixing from inside container (might work for some volumes)
echo ""
echo "📦 Method 1: Attempting to fix permissions inside container..."
docker exec -it $CONTAINER_NAME bash -c "
  echo 'Checking current permissions...'
  ls -la /app/generated/ 2>/dev/null || echo 'Directory not accessible'
  chmod -R 755 /app/generated 2>/dev/null && echo '✅ Permissions changed' || echo '❌ Permission change failed'
  chown -R appuser:appuser /app/generated 2>/dev/null && echo '✅ Ownership changed' || echo '❌ Ownership change failed'
" || echo "⚠️  Could not execute inside container"

# Method 2: Fix from host system
echo ""
echo "🏠 Method 2: Fixing permissions from host system..."
echo "   Note: Replace /path/to/your/app with your actual app path"

# Find the actual path where Docker volumes are mounted
echo ""
echo "🔍 Finding Docker volume paths..."
docker inspect $CONTAINER_NAME | grep -A 10 "Mounts" || echo "Could not inspect container"

echo ""
echo "💡 Manual steps to fix permissions:"
echo "   1. Find your Docker volume mount path:"
echo "      docker inspect $CONTAINER_NAME"
echo ""
echo "   2. On your host system, run:"
echo "      sudo chmod -R 755 /path/to/volume/generated/"
echo "      sudo chown -R 1000:1000 /path/to/volume/generated/"
echo ""
echo "   3. Or restart the container:"
echo "      docker-compose down"
echo "      docker-compose up -d"

# Method 3: Check if container is running and what user it's using
echo ""
echo "👤 Method 3: Checking container user..."
docker exec -it $CONTAINER_NAME whoami 2>/dev/null || echo "Could not check user"
docker exec -it $CONTAINER_NAME id 2>/dev/null || echo "Could not check user ID"

echo ""
echo "🎯 Quick fix commands (run these manually):"
echo "   # From host system:"
echo "   sudo find /var/lib/docker -name 'generated' -type d -exec chmod -R 755 {} \\; 2>/dev/null"
echo "   sudo find /var/lib/docker -name 'generated' -type d -exec chown -R 1000:1000 {} \\; 2>/dev/null"
