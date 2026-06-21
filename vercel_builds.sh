#!/bin/bash

echo "🚀 Starting Vercel build process..."

# Print environment for debugging (remove in production)
echo "🔍 Checking environment variables..."
echo "DATABASE_URL exists: $([ -n "$DATABASE_URL" ] && echo 'YES' || echo 'NO')"
echo "DATABASE_URL starts with: ${DATABASE_URL:0:15}..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Run Django commands
echo "📤 Running Django migrations..."
python manage.py makemigrations --noinput || echo "⚠️  Makemigrations failed, continuing..."
python manage.py migrate --noinput || echo "⚠️  Migrations failed, continuing..."

# Collect static files
echo "📤 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!"