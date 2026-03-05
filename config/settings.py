"""
Django settings for config project.
Finalized for B.Tech 4th Year Project: AI-Enabled Smart Digital Tourism Platform.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k0k92dc4dup@0tg^*u@ebb0s-0o+$dd5c8da^^9#6r(amex-$k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition - Includes all 4 modular apps planned
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Internal Project Apps [cite: 811, 1060]
    'accounts',      # User Auth, Profiles, & RBAC [cite: 815, 831]
    'destinations',  # Places, Guides, & Homestays [cite: 841, 855]
    'ai_engine',     # Sentiment ML & Trip Planning [cite: 894, 907]
    'services',      # Maps API, Chatbot, & Dynamic Feed [cite: 868, 915, 1207]
    'notifications',  # User Notifications & Alerts [cite: 1185, 1210]
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Global templates directory [cite: 958]
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notification_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database - Low-to-Moderate Complexity standard [cite: 1023, 1194]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


load_dotenv()
AI_API_KEY = os.getenv("AI_API_KEY")

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static and Media Files Configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model (Must be defined in accounts/models.py) 
AUTH_USER_MODEL = 'accounts.User'

# --- PROJECT SPECIFIC UI THEME SETTINGS (Light Theme Only) --- 

THEME_EMERALD = "#2E7D32"     # Lush Green (Nav/Headers) [cite: 1253]
THEME_GOLD = "#FFD700"        # Heritage Gold (Badges/Ratings) [cite: 883, 896]
THEME_SKY_WASH = "#F0F8FF"    # Light Cyan (Backgrounds) [cite: 715, 932]
THEME_CHARCOAL = "#333333"    # Typography [cite: 931]

# ----------------- EMAIL CONFIGURATION (SMTP) ----------------- # [cite: 611, 819, 922]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Credentials for Verification Logic
EMAIL_HOST_USER = 'harisaiparasa@gmail.com'
EMAIL_HOST_PASSWORD = 'zdiumjywpwxcvdbd'  

DEFAULT_FROM_EMAIL = 'Smart Tourism Support <harisaiparasa@gmail.com>'

EMAIL_TIMEOUT = 15


# Authentication Redirects [cite: 820, 821, 1137]
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'