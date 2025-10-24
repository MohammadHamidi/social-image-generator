# Docker Quick Start Guide

This guide shows you how to build and run the Social Image Generator using Docker with just a Dockerfile and `.env` file - **no docker-compose required**!

## Prerequisites

- Docker installed on your system
- Git (to clone the repository)

## Quick Start (3 Simple Steps)

### 1. Configure Environment

Create a `.env` file in the project root (or copy from the provided template):

```bash
cp .env.example .env  # Optional: modify settings as needed
```

The default `.env` file is already configured and ready to use!

### 2. Build the Docker Image

**Linux/Mac:**
```bash
./build.sh
```

**Windows:**
```cmd
build.bat
```

Or build manually:
```bash
docker build -t social-image-generator:latest .
```

### 3. Run the Container

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

Or run manually:
```bash
docker run -d \
  --name social-image-generator \
  --restart unless-stopped \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/generated:/app/generated \
  -e FLASK_ENV=production \
  social-image-generator:latest
```

**That's it!** The API is now available at `http://localhost:5000`

## Configuration Options

### Environment Variables (.env file)

The `.env` file contains all configuration options:

```bash
# Application Configuration
PORT=5000                          # API port (default: 5000)
FLASK_ENV=production              # Flask environment

# Docker Configuration
IMAGE_NAME=social-image-generator  # Docker image name
IMAGE_TAG=latest                   # Docker image tag
CONTAINER_NAME=social-image-generator  # Container name

# Volume Configuration (local directories)
UPLOADS_DIR=./uploads              # Uploaded images directory
OUTPUT_DIR=./output                # Generated images directory
GENERATED_DIR=./generated          # API-generated images directory
CONFIG_DIR=./config                # Configuration files directory

# Runtime Configuration
RESTART_POLICY=unless-stopped      # Docker restart policy

# Optional: Resource Limits
# MEMORY_LIMIT=2g                  # Memory limit (e.g., 2g, 512m)
# CPU_LIMIT=2                      # CPU limit (e.g., 2 for 2 CPUs)
```

### Customizing the Port

To run on a different port, modify the `PORT` variable in `.env`:

```bash
PORT=8080
```

Then rebuild and restart:
```bash
./build.sh
./run.sh
```

The API will be available at `http://localhost:8080`

## Common Operations

### View Container Logs

```bash
docker logs -f social-image-generator
```

### Stop the Container

```bash
docker stop social-image-generator
```

### Start the Container

```bash
docker start social-image-generator
```

### Restart the Container

```bash
docker restart social-image-generator
```

### Remove the Container

```bash
docker rm -f social-image-generator
```

### Rebuild and Restart

```bash
./build.sh
./run.sh
```

## Volume Mounts

The container uses the following volume mounts for persistent data:

| Host Directory | Container Directory | Purpose |
|---------------|-------------------|---------|
| `./uploads` | `/app/uploads` | Uploaded images (main, background, watermark) |
| `./output` | `/app/output` | Generated output images |
| `./generated` | `/app/generated` | API-generated images |

These directories are automatically created when you run `./run.sh` or `run.bat`.

## Health Check

The container includes a built-in health check that verifies Flask is running properly:

- **Interval**: Every 30 seconds
- **Timeout**: 10 seconds
- **Start Period**: 60 seconds (gives time for startup)
- **Retries**: 3

Check container health:
```bash
docker inspect --format='{{.State.Health.Status}}' social-image-generator
```

## Troubleshooting

### Container won't start

1. Check if port 5000 is already in use:
   ```bash
   # Linux/Mac
   lsof -i :5000

   # Windows
   netstat -ano | findstr :5000
   ```

2. View container logs:
   ```bash
   docker logs social-image-generator
   ```

3. Try running with a different port (modify `PORT` in `.env`)

### Permission issues (Linux)

If you encounter permission issues with volume mounts on Linux:

```bash
# Fix permissions for uploaded files
chmod -R 755 uploads output generated
```

### Build fails

1. Clear Docker build cache:
   ```bash
   docker builder prune
   ```

2. Rebuild from scratch:
   ```bash
   docker build --no-cache -t social-image-generator:latest .
   ```

### Container crashes immediately

1. Check logs for errors:
   ```bash
   docker logs social-image-generator
   ```

2. Verify all required files are present:
   ```bash
   ls -la src/ assets/ social_image_api.py requirements.txt
   ```

## Testing the API

Once the container is running, test the API:

```bash
# Check API health
curl http://localhost:5000/health

# Upload and generate an image (example)
curl -X POST http://localhost:5000/api/generate \
  -F "main_image=@/path/to/your/image.jpg" \
  -F "config=@/path/to/config.json"
```

See the full API documentation in `API_REFERENCE.md` and `COMPREHENSIVE_CURL_REFERENCE.md`.

## Production Deployment

### Security Recommendations

1. **Run as non-root user**: Already configured in Dockerfile (user: appuser)
2. **Resource limits**: Uncomment and set in `.env`:
   ```bash
   MEMORY_LIMIT=2g
   CPU_LIMIT=2
   ```
3. **Network isolation**: Consider using Docker networks
4. **Secrets management**: Use Docker secrets or environment variables for sensitive data

### Monitoring

Monitor container resource usage:
```bash
docker stats social-image-generator
```

### Backup

Backup your data directories regularly:
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz uploads/ output/ generated/ config/
```

## Comparison: Dockerfile vs Docker Compose

### Before (docker-compose)
```bash
docker-compose up -d
```

### Now (Dockerfile + .env)
```bash
./build.sh
./run.sh
```

**Benefits:**
- ✅ Simpler setup - no docker-compose installation needed
- ✅ Single `.env` file for all configuration
- ✅ Easy to understand and modify
- ✅ Works everywhere Docker is installed
- ✅ Easier to integrate with CI/CD pipelines

## Advanced Usage

### Manual Docker Commands

If you prefer manual control:

**Build:**
```bash
docker build -t social-image-generator:latest .
```

**Run:**
```bash
docker run -d \
  --name social-image-generator \
  --restart unless-stopped \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/generated:/app/generated \
  -e FLASK_ENV=production \
  -e PYTHONPATH=/app/src \
  -e PYTHONDONTWRITEBYTECODE=1 \
  social-image-generator:latest
```

### Using Different Image Tags

Build with a custom tag:
```bash
IMAGE_TAG=v1.0.0 ./build.sh
```

Run with a custom tag:
```bash
IMAGE_TAG=v1.0.0 ./run.sh
```

### Multiple Instances

Run multiple instances on different ports:

**Instance 1:**
```bash
docker run -d --name social-gen-1 -p 5001:5000 social-image-generator:latest
```

**Instance 2:**
```bash
docker run -d --name social-gen-2 -p 5002:5000 social-image-generator:latest
```

## Next Steps

- Read the [API Reference](API_REFERENCE.md) for detailed API documentation
- Check [COMPREHENSIVE_CURL_REFERENCE.md](COMPREHENSIVE_CURL_REFERENCE.md) for API examples
- Review [README.md](README.md) for project overview and features

## Support

If you encounter any issues:

1. Check the logs: `docker logs -f social-image-generator`
2. Review this guide's troubleshooting section
3. Open an issue on the GitHub repository
