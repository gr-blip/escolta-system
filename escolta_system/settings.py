"""
escolta_system/settings.py — versão segura e profissional
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mudanças em relação ao arquivo anterior:
  • SECRET_KEY lida de variável de ambiente (obrigatório em prod)
  • DEBUG vem de env; padrão False
  • ALLOWED_HOSTS lista fechada, sem '*'
  • Hardening HTTPS: SSL redirect, HSTS, cookies secure em prod
  • LOGGING básico para stdout (captura no Railway/Gunicorn)
  • Cache local para usar no @cache_page do dashboard

Dependência nova: python-decouple (pip install python-decouple)
"""

from pathlib import Path
import os
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ══════════════════════════════ SEGURANÇA ══════════════════════════════
SECRET_KEY = config('DJANGO_SECRET_KEY')  # NUNCA hardcoded
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS agora vem da env como lista separada por vírgula
ALLOWED_HOSTS = config(
    'DJANGO_ALLOWED_HOSTS',
    default='grupojr.up.railway.app,localhost,127.0.0.1',
    cast=Csv(),
)

CSRF_TRUSTED_ORIGINS = config(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    default='https://grupojr.up.railway.app',
    cast=Csv(),
)

# ══════════════════════════════ APPS ══════════════════════════════
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cadastros',
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

ROOT_URLCONF = 'escolta_system.urls'

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

WSGI_APPLICATION = 'escolta_system.wsgi.application'

# ══════════════════════════════ BANCO ══════════════════════════════
DATABASE_URL = config('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ══════════════════════════════ CACHE ══════════════════════════════
# Cache local em memória (suficiente para dashboard e omnilink).
# Em produção multi-worker, migrar para Redis.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'escolta-cache',
        'TIMEOUT': 300,
    }
}

# ══════════════════════════════ AUTH ══════════════════════════════
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ══════════════════════════════ I18N ══════════════════════════════
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ══════════════════════════════ STATIC / MEDIA ══════════════════════════════
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ══════════════════════════════ HARDENING HTTP ══════════════════════════════
# Só ativa em produção (DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # HSTS progressivo: começa em 60s (rollback fácil), aumentar após 1-2 semanas estáveis.
    # Próximos valores: 86400 (1 dia) → 2592000 (30 dias) → 31536000 (1 ano).
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False  # só ativar depois de 1 ano estável + hstspreload.org
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ══════════════════════════════ LOGGING ══════════════════════════════
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[{levelname}] {asctime} {name}: {message}', 'style': '{'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'cadastros': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}
