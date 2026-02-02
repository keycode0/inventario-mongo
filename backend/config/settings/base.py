from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==========================
# SEGURIDAD
# ==========================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-secret")

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# ==========================
# APPS
# ==========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",

    # Apps del proyecto
    "config.apps.users",
    "config.apps.inventory",
]

# ==========================
# MIDDLEWARE
# ==========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ==========================
# TEMPLATES
# ==========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==========================
# WSGI / ASGI
# ==========================
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ==========================
# DATABASE (temporal)
# ==========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==========================
# INTERNACIONALIZACIÓN
# ==========================
LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "es-ec")
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "America/Guayaquil")
USE_I18N = True
USE_TZ = True

# ==========================
# STATIC FILES
# ==========================
STATIC_URL = "/static/"

# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================
REST_FRAMEWORK = {
    # Autenticación global (JWT)
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "config.apps.users.authentication.JWTAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [],

    # API JSON only (profesional)
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],

    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# ============================================================
# DEFAULT FIELD
# ============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
