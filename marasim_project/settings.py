import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'marasim-secret-123'
DEBUG = True 
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',  # التصميم الفخم
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
    'django.contrib.sessions.middleware.SessionMiddleware', # لإدارة الجلسات
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'marasim_project.urls'
WSGI_APPLICATION = 'marasim_project.wsgi.application'

# --- إعدادات الأمان ومنع الدخول التلقائي ---
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # تسجيل خروج عند إغلاق المتصفح
SESSION_COOKIE_AGE = 3600  # تنتهي الجلسة بعد ساعة من الخمول
LOGIN_URL = '/admin/login/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# --- قاعدة البيانات ---
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

# --- إعدادات JAZZMIN المرنة للجوال (Responsive) ---
JAZZMIN_SETTINGS = {
    "site_title": "مراسيم الشموخ",
    "site_header": "مراسيم الشموخ",
    "site_brand": "المحاسب الذكي",
    "welcome_sign": "نظام مراسيم الشموخ المحاسبي",
    "copyright": "مراسيم الشموخ",
    "search_model": ["store.Product"],
    "show_sidebar": True,
    "navigation_expanded": False, # لجعل القائمة مخفية في الجوال تلقائياً
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "store.Product": "fas fa-tshirt",
        "store.Sale": "fas fa-cash-register",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lux", 
    "dark_mode_theme": "darkly",
    "navbar_fixed": True,  # تثبيت الشريط العلوي
    "sidebar_fixed": True, # تثبيت القائمة الجانبية
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_nav_compact_style": True, # ضغط العناصر لتناسب شاشة الجوال
    "sidebar_nav_child_indent": True,
    "body_small_text": True, # تصغير النصوص قليلاً لتجنب التداخل
}
