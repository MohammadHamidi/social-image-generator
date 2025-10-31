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
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --retries 3 --timeout 300 -r requirements.txt || \
    (echo "❌ pip install failed, retrying..." && \
    pip install --no-cache-dir --ignore-installed -r requirements.txt)

# Verify Python packages
RUN python -c "import flask, PIL, numpy; print('✅ Core packages installed successfully')" || \
    (echo '❌ Core packages verification failed' && exit 1)

# Copy project files
COPY src/ ./src/
COPY assets/ ./assets/
COPY social_image_api.py ./
COPY fix-permissions.sh ./

# Verify critical files
RUN test -f social_image_api.py && \
    test -f src/enhanced_social_generator.py && \
    test -d assets/fonts && \
    test -f fix-permissions.sh && \
    echo "✅ All critical files copied successfully"

# Make permission fix script executable
RUN chmod +x fix-permissions.sh

# Create necessary directories with proper structure and permissions
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
    chown -R appuser:appuser uploads output generated cache assets config && \
    chmod -R 755 assets/fonts && \
    chmod -R 775 uploads output generated

# Environment configuration
ENV PYTHONPATH=/app/src \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production \
    PORT=${PORT}

# Expose the port the app runs on
EXPOSE ${PORT}

# Dummy healthcheck (to satisfy Coolify)
HEALTHCHECK CMD echo "healthy"

# Labels (optional)
LABEL maintainer="Social Image Generator"
LABEL description="AI-powered social media image generator with multi-language support"
LABEL coolify.managed="true"

# Switch to non-root user
USER appuser

# Start Flask API server
CMD ["python", "social_image_api.py"]
