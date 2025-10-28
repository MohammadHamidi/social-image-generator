# Enhanced Social Media Image Generator Dockerfile
# Optimized for Coolify deployment
FROM python:3.11-slim

# Build arguments (can be overridden during build)
ARG PORT=5000

# Set working directory
WORKDIR /app

# Install system dependencies required for image processing and AI libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    libgl1 \
    libfreetype6-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl-dev \
    tk-dev \
    gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user FIRST (before copying files)
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Copy requirements and install Python dependencies with error handling
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --retries 3 --timeout 300 -r requirements.txt || \
    (echo "❌ pip install failed, retrying with different options..." && \
    pip install --no-cache-dir --ignore-installed --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt)

# Verify Python packages were installed correctly
RUN python -c "import flask, PIL, numpy; print('✅ Core packages installed successfully')" || \
    (echo "❌ Core packages verification failed" && exit 1)

# Copy project files with verification
COPY src/ ./src/
COPY assets/ ./assets/
COPY social_image_api.py ./
COPY fix-permissions.sh ./

# Verify critical files were copied
RUN test -f social_image_api.py && \
    test -f src/enhanced_social_generator.py && \
    test -d assets/fonts && \
    test -f fix-permissions.sh && \
    echo "✅ All critical files copied successfully" || \
    (echo "❌ Critical files missing after copy" && exit 1)

# Make permission fix script executable
RUN chmod +x fix-permissions.sh

# Create all necessary directories with proper structure
RUN mkdir -p \
    uploads/main \
    uploads/background \
    uploads/watermark \
    output \
    generated \
    cache/assets \
    cache/downloads \
    assets/fonts/downloaded \
    config && \
    # Set ownership for appuser
    chown -R appuser:appuser uploads output generated cache assets config && \
    # Ensure directories are fully writable by appuser
    chmod -R 755 assets/fonts && \
    chmod -R 775 uploads output generated

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV PORT=${PORT}

# Expose the port the app runs on (Coolify will detect this)
EXPOSE ${PORT}

# Health check - uses the Flask /health endpoint for proper monitoring
# Coolify will use this to verify the application is running correctly
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health').read()" || exit 1

# Labels for Coolify (optional but helpful)
LABEL maintainer="Social Image Generator"
LABEL description="AI-powered social media image generator with multi-language support"
LABEL coolify.managed="true"

# Switch to non-root user
USER appuser

# Default command - start Flask API server
CMD ["python", "social_image_api.py"]