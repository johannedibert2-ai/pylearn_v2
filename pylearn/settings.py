# ============================================================
# settings.py — Configuración principal del proyecto Django
# ============================================================
# ENLACE con el HTML:
#   - INSTALLED_APPS incluye 'runner', la app que maneja /run/
#   - TEMPLATES apunta a templates/runner/index.html (tu 1.html renombrado)
#   - STATIC_URL sirve los archivos CSS/JS si los separas en /static/
# ============================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️  En producción cambia esto a una clave secreta real y pon DEBUG=False
SECRET_KEY = 'django-insecure-pylearn-dev-key-cambia-esto-en-produccion'
DEBUG = True
ALLOWED_HOSTS = ['*']   # En producción pon tu dominio: ['pylearn.com']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'runner',   # ← tu app: contiene la vista /run/ y la página principal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    # CsrfViewMiddleware verifica el token {{ csrf_token }} del HTML
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pylearn.urls'   # ← apunta a pylearn/urls.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django buscará las plantillas en cada app/templates/
        'DIRS': [],
        'APP_DIRS': True,   # ← encuentra runner/templates/runner/index.html
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'pylearn.wsgi.application'

# Base de datos (no se usa en esta versión, pero Django la requiere)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Seguridad del ejecutor de código ──────────────────────────────────────────
# Tiempo máximo (segundos) que puede correr el código del usuario
CODE_TIMEOUT = 5
