from pathlib import Path
import os
import dj_database_url
# from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#load our environment 
#load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9+_@mp%sklldf6l7lq0o*1=h=y!y$@mb#n1#v(i4sptl-aoysm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("VERCEL_ENV") != "production"

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
        'DIRS': [],
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


DATABASES = {
    "default": dj_database_url.parse(
        "postgres://0f01eee13bd1de3195b7c50450320e4c9b3d8f20629c950a45f8104d53737d0d:sk_ZwN1_ZyG0Tpny3ko1gV85@db.prisma.io:5432/postgres?sslmode=require"
    )
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
STATICFILES_DIRS = [BASE_DIR / "Dyslexia_static_files"]
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


# Maximum size allowed for file uploads 
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000 
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000

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
