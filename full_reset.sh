#!/bin/bash

echo "🔧 COMPLETE DATABASE RESET"

# 1. Reset database using Python
echo "📤 Resetting database..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dyslexia.settings')
django.setup()
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('DROP SCHEMA public CASCADE;')
    cursor.execute('CREATE SCHEMA public;')
    cursor.execute('GRANT ALL ON SCHEMA public TO CURRENT_USER;')
    print('✅ Database reset!')
"

# 2. Delete migration files
echo "🗑️  Deleting migration files..."
rm -f casa/migrations/0*.py
rm -f pay/migrations/0*.py
rm -f cart/migrations/0*.py
rm -rf casa/migrations/__pycache__
rm -rf pay/migrations/__pycache__
rm -rf cart/migrations/__pycache__

# 3. Clear Django migration records
echo "📤 Clearing migration records..."
python manage.py migrate --fake 2>/dev/null || echo "⚠️  No migrations to clear"

# 4. Create fresh migrations
echo "📤 Creating fresh migrations..."
python manage.py makemigrations

# 5. Apply migrations
echo "📤 Applying migrations..."
python manage.py migrate

# 6. Show status
python manage.py showmigrations

echo "✅ Done!"
