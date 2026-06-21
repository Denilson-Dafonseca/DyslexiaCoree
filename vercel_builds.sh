#!/bin/bash
# vercel_build.sh

echo "🚀 Running Vercel build..."

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run Django migrations
python manage.py makemigrations
python manage.py migrate

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Generate Prisma client
npx prisma generate

# 5. Push Prisma schema (if needed)
npx prisma db push --accept-data-loss

echo "✅ Build complete!"