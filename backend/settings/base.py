import os
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

config_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(config_path):
    config.read(config_path)

SECRET_KEY = config('DJANGO_SECRET_KEY', default='Secreto')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'users',
    'documentos',
    'vencimientos',
    'programas',
]

THIRD_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'coreapi',
    # 'django_crontab',
    # 'dj_rest_auth',
    # 'rest_framework_simplejwt',
]


INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'GMT-3'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    ...: ...,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

TOKEN_EXPIRATION = config('TOKEN_EXPIRATION', default=5*60*60, cast=int)

# REST_FRAMEWORK = {
#     'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'dj_rest_auth.authentication.AllAuthJWTAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }

APPEND_SLASH = False

# Duración del token en segundos (por ejemplo, 30 días)
# TOKEN_EXPIRE = 5 * 60 * 60

# SIMPJWT = {
#     'USER_ID_FIELD': 'id',
#     'UPDATE_LAST_LOGIN': True,
# }

# CRONJOBS = [
#     ('0 0 * * *', 'users.tareas.enviar_correos'),
# ]
