# Dyslexia/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dyslexia.settings')

application = get_wsgi_application()

# Vercel expects an 'app' variable
app = application