#!/bin/bash
# fix_migrations_now.sh

echo "🔧 Fixing migrations..."

# 1. Reset casa migrations
echo "📤 Resetting casa migrations..."
python manage.py migrate casa zero --fake

# 2. Delete old casa migrations
echo "🗑️  Deleting old casa migrations..."
rm -f casa/migrations/0*.py
rm -rf casa/migrations/__pycache__

# 3. Create fresh casa migrations
echo "📤 Creating fresh casa migrations..."
python manage.py makemigrations casa

# 4. Apply casa migrations (creates tables)
echo "📤 Applying casa migrations..."
python manage.py migrate casa

# 5. Apply pay migrations
echo "📤 Applying pay migrations..."
python manage.py migrate pay

# 6. Apply sessions migrations
echo "📤 Applying sessions migrations..."
python manage.py migrate sessions

# 7. Show final status
python manage.py showmigrations


# Create static directory
mkdir -p static

# Install Python dependencies
pip install -r requirements.txt

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