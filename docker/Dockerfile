# Hermes Business OS — Docker Image
# Extends Hermes Agent with HBOS skills

FROM python:3.11-slim

LABEL maintainer="WS Capital AI Lab"
LABEL description="Hermes Business OS - AI operating system for SMBs"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libpango1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy HBOS files
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir \
    pyyaml \
    google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib \
    weasyprint

# Make scripts executable
RUN chmod +x /app/scripts/install.sh /app/scripts/test.sh

# Environment
ENV PYTHONPATH=/app/skills/hermes-business-core/tools:$PYTHONPATH
ENV HBOS_HOME=/app

# Expose port for dashboard (if needed)
EXPOSE 3000

# Default command
CMD ["bash", "-c", "echo 'Hermes Business OS installed. Run: hbos setup && hermes gateway start'"]
