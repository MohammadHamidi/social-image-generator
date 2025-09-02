# Linux Deployment Guide for Social Image Generator

## Overview

This document outlines the changes made to ensure seamless deployment on Linux systems when the project is pushed to GitHub and pulled on Linux environments.

## ✅ Compatibility Fixes Applied

### 1. Docker Compose Configuration

**File:** `docker-compose.yml`
- **Removed fixed user IDs**: Removed `user: "1000:1000"` specifications that assumed Windows user ID
- **Added configurable ports**: Changed ports to use environment variables (`${PORT:-5000}`)
- **Removed problematic named volumes**: Cleaned up unused volume definitions

### 2. Linux-Specific Configuration

**File:** `docker-compose.linux.yml`
- **Explicit user mapping**: `user: "1000:1000"` for typical Linux user
- **Volume permissions**: Added explicit read-write permissions (`:rw`)
- **Read-only config**: Made config directory read-only for security

### 3. Linux Build Script

**File:** `build-linux.sh`
- **Automatic port detection**: Checks if port 5000 is available
- **Directory creation**: Creates required directories with proper permissions
- **Linux-specific checks**: Validates Linux environment and dependencies
- **Alternative port handling**: Uses port 5001 if 5000 is occupied

### 4. Environment Configuration

**File:** `env.example`
- **Port configuration**: `PORT` and `DEV_PORT` variables
- **Build settings**: `BUILDKIT_PROGRESS` and `DOCKER_BUILDKIT` options
- **Volume permissions**: `VOLUME_PERMISSIONS` setting

### 5. PowerShell Script Updates

**File:** `test_docker.ps1`
- **Removed emoji characters**: Replaced with text equivalents for better compatibility
- **Cross-platform paths**: Uses consistent path handling

## 🚀 Linux Deployment Commands

### Option 1: Automated Build Script (Recommended)
```bash
# Make script executable
chmod +x build-linux.sh

# Run automated build
./build-linux.sh
```

### Option 2: Docker Compose with Linux Config
```bash
# Use Linux-specific configuration
docker-compose -f docker-compose.yml -f docker-compose.linux.yml up --build -d
```

### Option 3: Standard Docker Compose
```bash
# Basic deployment (should work on most Linux systems)
docker-compose up --build -d
```

### Option 4: Manual Docker Commands
```bash
# Build image
docker build -t social-image-generator .

# Run container with volume mounts
docker run -d -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/generated:/app/generated \
  -v $(pwd)/output:/app/output \
  social-image-generator
```

## 🔧 Potential Linux-Specific Issues & Solutions

### 1. User Permission Issues
**Problem:** Container user doesn't match host user ID
**Solution:** Use `docker-compose.linux.yml` which explicitly sets user ID

### 2. Port Conflicts
**Problem:** Port 5000 already in use by another service
**Solution:** The build script automatically detects and uses alternative ports

### 3. Volume Mount Permissions
**Problem:** Permission denied on mounted volumes
**Solution:** Linux config includes explicit permission specifications

### 4. File Permissions
**Problem:** Files created by container have wrong ownership
**Solution:** Use `docker-compose.linux.yml` with proper user mapping

## 📋 Verification Steps

After deployment, verify everything works:

```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs

# Test API health
curl http://localhost:5000/health

# Test gradient generation
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{"colors": ["#FF6B6B", "#4ECDC4"], "gradient_type": "linear"}'
```

## 🐧 Linux-Specific Features

1. **Automatic User Detection**: Scripts detect current user and adjust permissions
2. **Port Conflict Resolution**: Automatic port selection if defaults are unavailable
3. **Directory Permission Setup**: Proper permissions for volume mounts
4. **System Compatibility**: Works with various Linux distributions (Ubuntu, CentOS, etc.)

## 🔄 Environment Variables

Configure deployment with environment variables:

```bash
# Copy example environment file
cp env.example .env

# Edit configuration
nano .env

# Example .env content:
PORT=5000
DEV_PORT=8000
FLASK_ENV=production
VOLUME_PERMISSIONS=rw
```

## 📞 Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Check port usage
sudo lsof -i :5000

# Try different port
PORT=5001 docker-compose up -d
```

### Permission Errors
```bash
# Fix directory permissions
sudo chown -R $USER:$USER uploads generated output

# Use Linux-specific config
docker-compose -f docker-compose.yml -f docker-compose.linux.yml up --build -d
```

### Build Failures
```bash
# Clean build
docker-compose build --no-cache

# Check Docker resources
docker system df

# Free up space if needed
docker system prune -f
```

## ✅ Compatibility Status

- ✅ **Ubuntu 18.04+**: Fully supported
- ✅ **CentOS/RHEL 7+**: Fully supported
- ✅ **Debian 9+**: Fully supported
- ✅ **Docker 20.10+**: Required
- ✅ **Docker Compose 2.0+**: Required

## 🎯 Expected Outcome

After running `docker-compose up --build -d` on Linux, you should have:

1. ✅ Container running successfully
2. ✅ API accessible on configured port
3. ✅ Volume mounts working with proper permissions
4. ✅ All features functional (gradient generation, image processing, etc.)
5. ✅ No permission or user ID conflicts

The deployment should work seamlessly across different Linux environments with the provided configuration options.
