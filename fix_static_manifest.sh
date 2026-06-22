# 1. Create the missing file
echo "📁 Creating missing favicon.png..."
mkdir -p static/site/images
if [ -f site/images/favicon.png ]; then
    cp site/images/favicon.png static/site/images/
else
    # Create a simple favicon using Python
    python -c "
from PIL import Image
img = Image.new('RGB', (16, 16), color='#ffffff')
img.save('static/site/images/favicon.png')
" 2>/dev/null || echo "⚠️  Could not create favicon, creating empty file instead"
    touch static/site/images/favicon.png
fi

# 2. Remove old collected files
echo "🗑️  Removing old collected files..."
rm -rf staticfiles/

# 3. Collect static files
echo "📤 Collecting static files..."
python manage.py collectstatic --noinput --verbosity 1

# 4. Verify the file was collected
echo "🔍 Verifying collected files..."
ls -la staticfiles/site/images/ || echo "⚠️  File not collected!"

echo "✅ Done!"