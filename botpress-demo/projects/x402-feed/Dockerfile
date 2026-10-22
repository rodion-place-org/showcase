# x402 Forecast Endpoint - Production Dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
WORKDIR /home/app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py gunicorn_config.py ./

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-5001}/health', timeout=3)"

# Switch to non-root user
USER app

# Expose port
EXPOSE 5001

# Run with gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]