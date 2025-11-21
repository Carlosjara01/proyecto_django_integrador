from pathlib import Path
from django.contrib.messages import constants as messages

# ---------------------------------------
# BASE DIRECTORY
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# SECURITY
# ---------------------------------------
SECRET_KEY = 'django-insecure-reemplazar-esto-en-produccion'
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------------------------
# INSTALLED APPS
# ---------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App principal
    'core',

    # ⭐️ API y Documentación (AÑADIDO) ⭐️
    'rest_framework',       # Marco para construir APIs
    'drf_spectacular',      # Generador de esquemas OpenAPI para DRF
]

# ---------------------------------------
# MIDDLEWARE
# ---------------------------------------
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

# ---------------------------------------
# URL CONFIG
# ---------------------------------------
ROOT_URLCONF = 'tienda_integrador.urls'

# ---------------------------------------
# TEMPLATES
# ---------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates' 
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------------------------------
# WSGI / ASGI
# ---------------------------------------
WSGI_APPLICATION = 'tienda_integrador.wsgi.application'

# ---------------------------------------
# DATABASE (SQLite)
# ---------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------
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

# ---------------------------------------
# LANGUAGE, TIMEZONE
# ---------------------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Asuncion'
USE_I18N = True
USE_TZ = True

# ---------------------------------------
# STATIC FILES
# ---------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------------------
# MEDIA FILES
# ---------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------
# DEFAULT AUTO FIELD
# ---------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------
# LOGIN / LOGOUT CONFIG
# ---------------------------------------
LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'core:product_list'
LOGOUT_REDIRECT_URL = 'core:login'

# ---------------------------------------
# MESSAGES CONFIG
# ---------------------------------------
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ---------------------------------------
# ⭐️ DRF Configuration (AÑADIDO) ⭐️
# ---------------------------------------
REST_FRAMEWORK = {
    # Usar drf-spectacular como el generador de esquemas por defecto
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ---------------------------------------
# ⭐️ DRF SPECTACULAR SETTINGS (AÑADIDO) ⭐️
# ---------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Tienda Integrador API',
    'DESCRIPTION': 'Documentación interactiva de la API para la gestión de la tienda.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, # No incluir la ruta del esquema en el esquema generado
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True, # Mantener la autorización al recargar
    },
}