#!/bin/bash

echo "🚀 Setting up Sahool Project..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ Please edit .env file with your CDSE credentials"
fi

# Create storage directories
echo "📁 Creating storage directories..."
mkdir -p storage/sentinel
mkdir -p storage/ndvi
mkdir -p storage/ndvi_previews
mkdir -p storage/delta_ndvi
mkdir -p storage/tiles

# Start Docker containers
echo "🐳 Starting Docker containers..."
docker compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker compose exec -T api alembic upgrade head

echo "✅ Setup complete!"
echo ""
echo "📊 Access Swagger API documentation at: http://localhost:8000/docs"
echo "📦 Access storage files at: http://localhost:8000/storage/"
echo ""
echo "To stop the application, run: docker compose down"
