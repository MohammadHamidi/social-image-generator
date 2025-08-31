# Enhanced Social Media Image Generator Dockerfile
FROM python:3.11-slim

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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user FIRST (before copying files)
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY assets/ ./assets/
COPY social_image_api.py ./

# Create directories and set proper permissions
RUN mkdir -p uploads/main uploads/background uploads/watermark output generated && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production

# Health check - simple import test
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import flask; print('OK')" || exit 1

# Default command - start Flask API server
CMD ["python", "social_image_api.py"]