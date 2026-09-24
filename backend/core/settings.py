"""
Configuración de Django para el proyecto core (BiomecanicSport).
Arquitectura basada en Microservicios: Backend API REST.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Directorio base del proyecto backend (/app en contenedor o ./backend en local)
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde el archivo .env en la raíz o en backend
load_dotenv(BASE_DIR.parent / '.env')
load_dotenv(BASE_DIR / '.env')

# Clave secreta (definida en .env para entornos productivos)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-me')

# Modo depuración (True en desarrollo, False en producción)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,backend').split(',')


# ==========================================
# DEFINICIÓN DE APLICACIONES INSTALADAS
# ==========================================

INSTALLED_APPS = [
    # Aplicaciones estándar de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías de terceros
    'rest_framework',
    'corsheaders',

    # Aplicaciones del proyecto
    'core_app',
]

# ==========================================
# MIDDLEWARES
# ==========================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Procesamiento de CORS (al inicio)
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'


# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS (PostgreSQL)
# ==========================================

POSTGRES_DB = os.getenv('POSTGRES_DB', 'BiomecanicSport')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'biomecanic_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'biomecanic_secret_password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}


# ==========================================
# CONFIGURACIÓN DE CACHÉ (Redis)
# ==========================================

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
    }
}


# ==========================================
# VALIDACIÓN DE CONTRASEÑAS
# ==========================================

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


# ==========================================
# INTERNACIONALIZACIÓN Y ZONA HORARIA
# ==========================================

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


# ==========================================
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# ==========================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================
# CONFIGURACIÓN DJANGO REST FRAMEWORK & CORS
# ==========================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Habilitar CORS para permitir peticiones desde React Native y entornos web
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True

# URL interna para comunicación con el Microservicio de Machine Learning
ML_SERVICE_URL = f"http://{os.getenv('ML_SERVICE_HOST', 'ml_service')}:{os.getenv('ML_SERVICE_PORT', '8001')}"
