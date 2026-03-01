import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'marasim-secret-123'
DEBUG = True 
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',  # يجب أن تكون في البداية لتغيير التصميم
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'marasim_project.urls'
WSGI_APPLICATION = 'marasim_project.wsgi.application'

# إعدادات قاعدة البيانات لمنع "تعليق التحميل"
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=0,
        conn_health_checks=True,
    )
}

TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','APP_DIRS': True,
              'OPTIONS': {'context_processors': ['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- إعدادات التصميم العصري (JAZZMIN) ---
JAZZMIN_SETTINGS = {
    "site_title": "مراسيم الشموخ",
    "site_header": "مراسيم الشموخ",
    "site_brand": "المحاسب الذكي",
    "welcome_sign": "أهلاً بك في نظام إدارة مراسيم الشموخ",
    "copyright": "مراسيم الشموخ للملابس",
    "search_model": ["store.Product"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "store.Product": "fas fa-tshirt",
        "store.Sale": "fas fa-cash-register",
    },
    "order_with_respect_to": ["store", "store.Product", "store.Sale"],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lux",  # ثيم فخم أسود وأبيض
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
}
