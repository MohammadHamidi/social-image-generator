#!/bin/bash
# Fix volume permissions for Docker on Windows
# This script runs as root to fix permissions, then switches to appuser

echo "🔧 Fixing Docker volume permissions..."

# Fix permissions for mounted volumes
if [ -d "/app/uploads" ]; then
    echo "📁 Fixing uploads directory permissions..."
    chmod -R 755 /app/uploads 2>/dev/null || echo "⚠️  Could not fix uploads permissions"
fi

if [ -d "/app/generated" ]; then
    echo "📁 Fixing generated directory permissions..."
    chmod -R 755 /app/generated 2>/dev/null || echo "⚠️  Could not fix generated permissions"
fi

if [ -d "/app/output" ]; then
    echo "📁 Fixing output directory permissions..."
    chmod -R 755 /app/output 2>/dev/null || echo "⚠️  Could not fix output permissions"
fi

echo "✅ Permission fixes applied"

# Now switch to appuser and run the application
echo "👤 Switching to appuser..."
exec gosu appuser "$@"
