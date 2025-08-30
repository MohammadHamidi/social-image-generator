# Dockerfile for Social Image Generator
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fontconfig \
    libfreetype6-dev \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy font files to system fonts directory
COPY assets/fonts/*.ttf /usr/share/fonts/truetype/custom/

# Update font cache
RUN fc-cache -fv

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads/main uploads/watermark uploads/background generated output

# Set environment variables
ENV PYTHONPATH=/app/src
ENV FLASK_APP=social_image_api.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
