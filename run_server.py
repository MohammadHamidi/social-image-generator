#!/usr/bin/env python3
"""
Script to run the Social Image Generator API Server
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import PIL
        import rembg
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def main():
    """Main function to run the server"""
    print("🚀 Social Image Generator API Server Launcher")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists('social_image_api.py'):
        print("❌ Error: social_image_api.py not found")
        print("Please run this script from the social-image-generator directory")
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Ensure upload directories exist
    os.makedirs('uploads/main', exist_ok=True)
    os.makedirs('uploads/watermark', exist_ok=True)
    os.makedirs('generated', exist_ok=True)

    print("📁 Upload directories ready:")
    print("   • uploads/main/ - Main images")
    print("   • uploads/watermark/ - Watermark images")
    print("   • generated/ - Generated images")

    print()
    print("🌐 Starting server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("📖 API Documentation: http://localhost:5000")
    print("💡 Health Check: http://localhost:5000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)

    try:
        # Run the Flask server
        subprocess.run([sys.executable, 'social_image_api.py'], check=True)
    except KeyboardInterrupt:
        print()
        print("🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
