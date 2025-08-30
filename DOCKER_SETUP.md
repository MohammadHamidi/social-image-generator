# 🐳 Docker Setup for Social Image Generator

This guide helps you set up the social image generator as a self-contained Docker service with bundled fonts.

## 📋 Prerequisites

- Docker installed on your system
- Python 3.11+ (for local testing)

## 🔤 Font Setup

The service requires fonts for multilingual text rendering. You have several options:

### Option 1: Download Bundled Fonts (Recommended)

```bash
# Download fonts automatically
python3 download_fonts.py

# Or manually download and place in assets/fonts/:
# - NotoSans-Regular.ttf
# - NotoSans-Bold.ttf  
# - NotoSansArabic-Regular.ttf
# - NotoSansArabic-Bold.ttf
```

### Option 2: Use Alternative Fonts

Place any TTF fonts with Arabic and Latin support in `assets/fonts/`:
- **Inter** (modern UI font)
- **Source Sans Pro** (Adobe)
- **Roboto** (Google)
- **IBM Plex Sans** (includes Arabic)

### Option 3: System Fonts (Development Only)

For local development, the system will use system fonts automatically.

## 🏗️ Building the Docker Image

```bash
# Build the image
docker build -t social-image-generator .

# Or with a specific tag
docker build -t social-image-generator:latest .
```

## 🚀 Running the Container

### Basic Run

```bash
docker run -p 5000:5000 social-image-generator
```

### With Volume Mounts (Recommended)

```bash
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/generated:/app/generated \
  -v $(pwd)/output:/app/output \
  social-image-generator
```

### With Environment Variables

```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e PYTHONPATH=/app/src \
  -v $(pwd)/uploads:/app/uploads \
  social-image-generator
```

## 🔧 Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  social-image-generator:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./generated:/app/generated
      - ./output:/app/output
    environment:
      - FLASK_ENV=production
      - PYTHONPATH=/app/src
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Run with:
```bash
docker-compose up -d
```

## 📊 Testing the Setup

### 1. Test Font System
```bash
# Before building Docker image
python3 test_docker_fonts.py
```

### 2. Test Container Health
```bash
# After running container
curl http://localhost:5000/health
```

### 3. Test API Endpoints
```bash
# Generate text layout
curl -X POST http://localhost:5000/generate_text \
  -H "Content-Type: application/json" \
  -d '{"layout_type": "quote", "content": {"quote": "Hello Docker!"}}'

# Get layout info
curl http://localhost:5000/text_layout_info
```

## 📁 Directory Structure in Container

```
/app/
├── src/                    # Source code
├── assets/fonts/           # Bundled fonts
├── config/                 # Configuration files
├── uploads/               # Uploaded images (mounted)
├── generated/             # Generated images (mounted)
├── output/                # Output directory (mounted)
├── social_image_api.py    # Flask API
└── requirements.txt       # Dependencies
```

## 🔧 Container Configuration

### Font Installation
The Dockerfile installs fonts in `/usr/share/fonts/truetype/custom/` and updates the font cache with `fc-cache -fv`.

### System Dependencies
- `fontconfig` - Font management
- `libfreetype6-dev` - Font rendering
- `libjpeg-dev` - JPEG support
- `libpng-dev` - PNG support
- `libwebp-dev` - WebP support

### Python Dependencies
All Python packages are installed from `requirements.txt`.

## 🎯 Production Deployment

### 1. Multi-stage Build (Optional)

```dockerfile
# Build stage
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
# ... rest of Dockerfile
```

### 2. Health Checks

The container includes health checks:
```bash
docker ps  # Check health status
```

### 3. Resource Limits

```bash
docker run --memory=512m --cpus=1.0 -p 5000:5000 social-image-generator
```

## 📋 API Endpoints

Once running, the service provides:

- `GET /` - API documentation
- `GET /health` - Health check
- `POST /generate_text` - Generate text layouts
- `POST /generate_all_text` - Generate all text layouts
- `GET /text_layout_info` - Layout documentation
- `POST /upload/main` - Upload main images
- `POST /upload/watermark` - Upload watermarks
- `POST /generate` - Generate with images

## 🔍 Troubleshooting

### Font Issues
```bash
# Check fonts in container
docker exec -it <container_id> fc-list | grep -i noto

# Check font files
docker exec -it <container_id> ls -la /usr/share/fonts/truetype/custom/
```

### Permission Issues
```bash
# Fix volume permissions
sudo chown -R $USER:$USER uploads generated output
```

### Memory Issues
```bash
# Monitor resource usage
docker stats <container_id>
```

### API Issues
```bash
# Check container logs
docker logs <container_id>

# Check Flask debug mode
docker run -e FLASK_ENV=development social-image-generator
```

## 🎉 Complete Example

```bash
# 1. Setup
git clone <repository>
cd social-image-generator

# 2. Download fonts
python3 download_fonts.py

# 3. Test locally
python3 test_docker_fonts.py

# 4. Build and run
docker build -t social-image-generator .
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  social-image-generator

# 5. Test API
curl http://localhost:5000/health
```

Your social image generator is now running as a self-contained Docker service! 🚀
