#!/bin/bash
# Hermes Business OS - Setup Script
# Run this after cloning the repository

set -e

echo "🚀 Hermes Business OS - Setup"
echo "=============================="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker found"

# Create directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p output
mkdir -p config
mkdir -p logs

# Copy config files
echo "⚙️  Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env - Please edit with your credentials"
fi

if [ ! -f config/client.yaml ]; then
    cp config/client.yaml.example config/client.yaml
    echo "📝 Created config/client.yaml - Please customize for your business"
fi

# Create Google service account placeholder
if [ ! -f config/google-service-account.json ]; then
    echo "{}" > config/google-service-account.json
    echo "📝 Created placeholder for Google service account JSON"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials (TELEGRAM_BOT_TOKEN, etc.)"
echo "2. Edit config/client.yaml for your business"
echo "3. Add your Google service account JSON to config/"
echo "4. Run: docker-compose -f docker/docker-compose.yml up -d"
echo ""
echo "For help, see docs/quickstart.md"
