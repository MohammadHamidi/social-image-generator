#!/usr/bin/env python3
"""
Validation script to check if the Social Image Generator setup is ready for Docker build.
This script verifies all dependencies and configuration before attempting to build.
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path

def print_status(status, message):
    """Print colored status messages"""
    colors = {
        'success': '\033[92m',  # Green
        'warning': '\033[93m',  # Yellow
        'error': '\033[91m',    # Red
        'info': '\033[94m'      # Blue
    }
    reset = '\033[0m'
    symbol = {
        'success': '✅',
        'warning': '⚠️',
        'error': '❌',
        'info': 'ℹ️'
    }
    print(f"{colors.get(status, colors['info'])}{symbol.get(status, 'ℹ️')} {message}{reset}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_status('success', f"{description} found: {filepath}")
        return True
    else:
        print_status('error', f"{description} missing: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print_status('success', f"{description} exists: {dirpath}")
        return True
    else:
        print_status('warning', f"{description} missing: {dirpath}")
        return False

def check_python_import(module_name, description):
    """Check if a Python module can be imported"""
    try:
        importlib.import_module(module_name)
        print_status('success', f"{description} available: {module_name}")
        return True
    except ImportError as e:
        print_status('warning', f"{description} not available: {module_name} ({e})")
        return False

def check_font_files():
    """Check if required font files exist"""
    font_dir = "assets/fonts"
    required_fonts = [
        "IRANYekanBoldFaNum.ttf",
        "IRANYekanMediumFaNum.ttf",
        "IRANYekanRegularFaNum.ttf",
        "NotoSans-Bold.ttf",
        "NotoSans-Regular.ttf",
        "NotoSansArabic-Bold.ttf",
        "NotoSansArabic-Regular.ttf"
    ]

    if not check_directory_exists(font_dir, "Fonts directory"):
        return False

    missing_fonts = 0
    for font in required_fonts:
        font_path = os.path.join(font_dir, font)
        if not os.path.exists(font_path):
            print_status('warning', f"Font file missing: {font}")
            missing_fonts += 1

    if missing_fonts == 0:
        print_status('success', "All required font files present")
        return True
    else:
        print_status('warning', f"{missing_fonts} font files missing - text rendering may be limited")
        return missing_fonts < len(required_fonts)  # Allow some fonts to be missing

def validate_python_syntax():
    """Validate Python syntax of key files"""
    python_files = [
        "social_image_api.py",
        "src/enhanced_social_generator.py"
    ]

    syntax_ok = True
    for pyfile in python_files:
        if check_file_exists(pyfile, "Python file"):
            try:
                with open(pyfile, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, pyfile, 'exec')
                print_status('success', f"Python syntax OK: {pyfile}")
            except SyntaxError as e:
                print_status('error', f"Python syntax error in {pyfile}: {e}")
                syntax_ok = False
            except Exception as e:
                print_status('error', f"Error reading {pyfile}: {e}")
                syntax_ok = False
        else:
            syntax_ok = False

    return syntax_ok

def check_docker_setup():
    """Check if Docker is available and properly configured"""
    try:
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_status('success', f"Docker available: {version}")
        else:
            print_status('error', "Docker not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_status('error', "Docker not found or not accessible")
        return False

    # Check if Docker daemon is running
    try:
        result = subprocess.run(['docker', 'info'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_status('success', "Docker daemon is running")
            return True
        else:
            print_status('error', "Docker daemon is not running")
            return False
    except subprocess.TimeoutExpired:
        print_status('error', "Docker daemon check timed out")
        return False

def main():
    """Main validation function"""
    print("🔍 Social Image Generator Setup Validation")
    print("=" * 50)

    all_checks_passed = True

    # Check required files
    print("\n📁 Checking Files and Directories...")
    required_files = [
        ("Dockerfile", "Dockerfile"),
        ("requirements.txt", "Requirements file"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("social_image_api.py", "Main API file"),
        ("src/enhanced_social_generator.py", "Generator module")
    ]

    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_checks_passed = False

    # Check directories
    required_dirs = [
        ("assets", "Assets directory"),
        ("assets/fonts", "Fonts directory"),
        ("uploads", "Uploads directory"),
        ("uploads/main", "Main uploads directory"),
        ("uploads/watermark", "Watermark uploads directory"),
        ("uploads/background", "Background uploads directory"),
        ("generated", "Generated images directory"),
        ("output", "Output directory")
    ]

    for dirpath, description in required_dirs:
        if not check_directory_exists(dirpath, description):
            # Try to create missing directories
            try:
                os.makedirs(dirpath, exist_ok=True)
                print_status('success', f"Created missing directory: {dirpath}")
            except Exception as e:
                print_status('error', f"Failed to create directory {dirpath}: {e}")
                all_checks_passed = False

    # Check font files
    print("\n🔤 Checking Font Files...")
    if not check_font_files():
        all_checks_passed = False

    # Validate Python syntax
    print("\n🐍 Validating Python Syntax...")
    if not validate_python_syntax():
        all_checks_passed = False

    # Check Python dependencies (if available)
    print("\n📦 Checking Python Dependencies...")
    optional_deps = [
        ("PIL", "Pillow (PIL)"),
        ("flask", "Flask"),
        ("numpy", "NumPy"),
        ("requests", "Requests"),
        ("flask_cors", "Flask-CORS")
    ]

    for module, description in optional_deps:
        check_python_import(module, description)

    # Check Docker setup
    print("\n🐳 Checking Docker Setup...")
    docker_ok = check_docker_setup()
    if not docker_ok:
        all_checks_passed = False

    # Final summary
    print("\n" + "=" * 50)
    if all_checks_passed:
        print_status('success', "All validation checks passed! Ready to build Docker container.")
        print("\n🚀 Build commands:")
        print("   docker-compose build")
        print("   docker-compose build --no-cache  # Force fresh build")
        print("   ./test_docker.sh                 # Build and test automatically")
        return 0
    else:
        print_status('error', "Some validation checks failed. Please fix the issues above before building.")
        print("\n💡 Common fixes:")
        print("   - Ensure Docker Desktop is running")
        print("   - Check that all required files are present")
        print("   - Verify Python syntax in source files")
        print("   - Ensure sufficient disk space (>5GB)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
