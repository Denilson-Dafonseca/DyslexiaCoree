import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'He3Erj7PPQvaeHLDPdE5mP7EAqUQ07oyy67bcQClEIVLtzcp0tcrCtQ1LhRq8MwhMsI'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [".vercel.app",'dyslexia-coree.vercel.app', 'dyslexiacore.xyz']

CSRF_TRUSTED_ORIGINS = ['https://dyslexia-coree.vercel.app', 'https://dyslexiacore.xyz']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'casa',
    'cart',
    'pay',
    'whitenoise.runserver_nostatic',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'Dyslexia.middleware.RateLimitMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
]

ROOT_URLCONF = 'Dyslexia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'Dyslexia.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASE_URL = (
    os.getenv('DATABASE_URL') or 
    os.getenv('POSTGRES_URL') or 
    os.getenv('PRISMA_DATABASE_URL') or 
    ''
).strip()

# Debug: Print to logs
print(f"🔍 DATABASE_URL found: {'YES' if DATABASE_URL else 'NO'}")
if DATABASE_URL:
    print(f"🔍 DATABASE_URL starts with: {DATABASE_URL[:20]}...")

# Force PostgreSQL if on Vercel or if DATABASE_URL exists
if DATABASE_URL and DATABASE_URL.startswith(('postgres://', 'postgresql://')):
    try:
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
        print("✅ Using PostgreSQL database")
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '/tmp/db.sqlite3',
            }
        }
else:
    # Only use SQLite if explicitly set or local development
    if os.getenv('VERCEL'):
        print("❌ ERROR: DATABASE_URL not set on Vercel!")
        # Don't fallback to SQLite on Vercel - fail explicitly
        raise Exception("DATABASE_URL environment variable is required on Vercel")
    else:
        print("⚠️  Using SQLite (local development)")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Windhoek'

USE_I18N = True

USE_TZ = True

# STATIC FILES
# -------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "Dyslexia_static_files"
] if (BASE_DIR / "Dyslexia_static_files").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------
# MEDIA FILES

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30

EMAIL_HOST_USER = os.getenv("BREVO_SMTP_LOGIN")
EMAIL_HOST_PASSWORD = os.getenv("BREVO_SMTP_KEY")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

DEFAULT_FROM_EMAIL = "noreply@dyslexiacore.com"