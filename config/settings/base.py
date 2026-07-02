from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'unsafe-dev-key-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'apps.core',
    'apps.accounts',
    'apps.customers',
    'apps.catalog',
    'apps.estimates',
    'apps.service_reports',
    'apps.inventory',
    'apps.sales',
    'apps.finance',
    'apps.saas',
    'apps.schools',
    'apps.academics',
    'apps.students',
    'apps.guardians',
    'apps.attendance',
    'apps.agents',
    'apps.escola_segura_assistant',
    'apps.policy_guard',
    'apps.integrations',
    'apps.pages',
    'apps.public_site',
    'apps.backoffice',
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.RequestAuditMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
    }
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

import sys

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'smart_system_base'),
        'USER': os.getenv('POSTGRES_USER', 'smart_system'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'smart_system_password'),
        'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 60,
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Django Axes settings
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # 1 hora de bloqueio
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']
AXES_RESET_ON_SUCCESS = True
AXES_ENABLED = 'test' not in sys.argv


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'America/Sao_Paulo')
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage' if 'test' not in sys.argv else 'django.contrib.staticfiles.storage.StaticFilesStorage'
    },
}
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.core.api.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
}

# ── E-mail e configuração do Atlas ──────────────────────────────────────────
# Quando AGENTS_EMAIL_DRY_RUN=true (padrão em desenvolvimento), o Django
# imprime o e-mail no console em vez de enviar de verdade.  Nenhuma
# credencial SMTP é exigida nesse modo.
#
# Para produção, defina AGENTS_EMAIL_DRY_RUN=false no .env e preencha
# as variáveis de SMTP abaixo.
AGENTS_EMAIL_DRY_RUN = os.getenv('AGENTS_EMAIL_DRY_RUN', 'true').lower() == 'true'

if AGENTS_EMAIL_DRY_RUN:
    # Modo desenvolvimento / teste: e-mails só aparecem no terminal
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Modo produção: envio real via SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST          = os.getenv('EMAIL_HOST', '')           # ex: smtp.gmail.com
    EMAIL_PORT          = int(os.getenv('EMAIL_PORT', '587'))   # 587=TLS, 465=SSL
    EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS', 'true').lower() == 'true'
    EMAIL_USE_SSL       = os.getenv('EMAIL_USE_SSL', 'false').lower() == 'true'
    # EMAIL_USE_TLS e EMAIL_USE_SSL são mutuamente exclusivos.
    # Use TLS (587) para Gmail/Zoho/Titan; SSL (465) somente se o provedor exigir.
    EMAIL_TIMEOUT = 10  # segundos — evita hang em caso de SMTP lento

DEFAULT_FROM_EMAIL    = os.getenv('DEFAULT_FROM_EMAIL', 'nao-responda@smart-system.local')
ATLAS_DEFAULT_FROM_EMAIL = os.getenv('ATLAS_DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
POLICY_GUARD_STRICT_MODE = os.getenv('POLICY_GUARD_STRICT_MODE', 'true').lower() == 'true'

# ── Assistente EscolaSegura ────────────────────────────────────────────────────
SANTANDER_ASSISTANT_ENABLED = os.getenv('SANTANDER_ASSISTANT_ENABLED', 'true').lower() == 'true'
SANTANDER_AI_PROVIDER = os.getenv('SANTANDER_AI_PROVIDER', 'fallback')   # 'gemini' ou 'fallback'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
SANTANDER_AI_MODEL = os.getenv('SANTANDER_AI_MODEL', 'gemini-2.0-flash')
SANTANDER_AI_TEMPERATURE = float(os.getenv('SANTANDER_AI_TEMPERATURE', '0.4'))
SANTANDER_AI_MAX_TOKENS = int(os.getenv('SANTANDER_AI_MAX_TOKENS', '500'))
SANTANDER_CHAT_MAX_MESSAGE_LENGTH = int(os.getenv('SANTANDER_CHAT_MAX_MESSAGE_LENGTH', '2000'))

SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'false').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'false').lower() == 'true'
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
REFERRER_POLICY = 'same-origin'

LOGIN_URL = '/app/login/'
LOGIN_REDIRECT_URL = '/app/'
LOGOUT_REDIRECT_URL = '/app/login/'

# Webhook para envio de leads qualificados da Assistente EscolaSegura
ESCOLA_SEGURA_LEAD_WEBHOOK_URL = os.getenv('ESCOLA_SEGURA_LEAD_WEBHOOK_URL', '')

