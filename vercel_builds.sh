#!/bin/bash

# Create static directory
mkdir -p newFiles

# Collect static files
echo "📤 Collecting static files..."
python manage.py collectstatic --noinput

# Show collected files
echo "📊 Collected static files:"
ls -la staticfiles/ || echo "⚠️  No static files found"

# Run migrations
echo "📤 Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "✅ Build completed successfully!"