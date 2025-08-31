#!/bin/bash
set -e

echo "🚀 Social Image Generator - Container Startup"
echo "=============================================="

# Function to safely create directories
create_directory() {
    local dir_path="$1"
    local dir_name="$2"
    
    echo "📁 Checking directory: $dir_path"
    
    if [ -d "$dir_path" ]; then
        echo "   ✅ Directory exists: $dir_path"
        
        # Check if we can write to it
        if [ -w "$dir_path" ]; then
            echo "   ✅ Write permission OK: $dir_path"
        else
            echo "   ⚠️  No write permission: $dir_path"
            echo "   🔧 Attempting to fix permissions..."
            
            # Try to fix permissions (will fail silently if not possible)
            chmod u+w "$dir_path" 2>/dev/null || true
            
            # Check again
            if [ -w "$dir_path" ]; then
                echo "   ✅ Permissions fixed: $dir_path"
            else
                echo "   ❌ Could not fix permissions: $dir_path"
                echo "   💡 This might cause issues with file uploads"
            fi
        fi
    else
        echo "   📂 Creating directory: $dir_path"
        if mkdir -p "$dir_path" 2>/dev/null; then
            echo "   ✅ Created successfully: $dir_path"
        else
            echo "   ❌ Failed to create: $dir_path"
            echo "   💡 Python will attempt to create this during runtime"
        fi
    fi
}

# Create all required directories
echo ""
echo "📋 Setting up directory structure..."

create_directory "/app/uploads" "uploads root"
create_directory "/app/uploads/main" "main images"
create_directory "/app/uploads/watermark" "watermark images"  
create_directory "/app/uploads/background" "background images"
create_directory "/app/output" "output/generated images"
create_directory "/app/generated" "generated images (API)"

# Check Python environment
echo ""
echo "🐍 Checking Python environment..."
echo "   Python version: $(python --version)"
echo "   Working directory: $(pwd)"
echo "   User: $(whoami)"
echo "   User ID: $(id -u)"
echo "   Group ID: $(id -g)"

# Check if critical Python modules can be imported
echo ""
echo "📦 Checking Python dependencies..."

python -c "
import sys
modules_to_check = [
    'PIL', 'numpy', 'flask', 'arabic_reshaper', 
    'bidi', 'rembg', 'onnxruntime'
]

for module in modules_to_check:
    try:
        __import__(module)
        print(f'   ✅ {module}')
    except ImportError as e:
        print(f'   ❌ {module}: {e}')
        sys.exit(1)
"

# Check if our custom module can be imported
echo "   🔍 Checking custom modules..."
python -c "
try:
    from src.enhanced_social_generator import EnhancedSocialImageGenerator
    print('   ✅ enhanced_social_generator')
except ImportError as e:
    print(f'   ❌ enhanced_social_generator: {e}')
    print('   💡 Check PYTHONPATH and file locations')
    exit(1)
"

echo ""
echo "🏁 Startup checks complete!"
echo "🚀 Starting Flask API server..."
echo ""

# Start the main application
exec python social_image_api.py