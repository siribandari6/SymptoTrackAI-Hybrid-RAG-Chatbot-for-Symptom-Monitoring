# Use Python 3.8 slim image for optimal compatibility
FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UV using pip (more reliable in Docker than curl script)
RUN pip install --no-cache-dir uv

# Set UV timeout to 5 minutes for large packages (like nvidia-cudnn 531MB)
ENV UV_HTTP_TIMEOUT=300

# Copy requirements first for better caching
COPY requirements.txt .

# Create virtual environment using UV and install dependencies
# Increased timeout handles large PyTorch CUDA dependencies
RUN uv venv /app/.venv && \
    . /app/.venv/bin/activate && \
    uv pip install -r requirements.txt

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/media

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000
