# Enhanced Social Media Image Generator Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (including Flask)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional ML/AI dependencies
RUN pip install --no-cache-dir \
    rembg \
    onnxruntime \
    scipy \
    numpy

# Copy project files
COPY src/ ./src/
COPY assets/ ./assets/
COPY social_image_api.py ./
COPY run_server.py ./

# Create necessary directories only

# Create necessary directories
RUN mkdir -p uploads/main uploads/background uploads/watermark output

# Set Python path
ENV PYTHONPATH=/app/src

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.enhanced_social_generator import EnhancedSocialImageGenerator; generator = EnhancedSocialImageGenerator(); print('OK')" || exit 1

# Default command - start Flask API server
CMD ["python", "social_image_api.py"]