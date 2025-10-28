from pathlib import Path

from django.utils.csp import CSP

# Directory paths

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = BASE_DIR / "app"

ASSETS_DIR = APP_DIR / "assets"


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",  # (depends on auth, sessions, messages, contenttypes)
    "django.contrib.staticfiles",
    # UI & Styling
    "djangx.tailwindcss",
    "djangx.components",
    # Authentication extensions (after django.contrib.auth, djangx.components)
    "phonenumber_field",
    "djangx.authx",
    # Admin extensions
    "djangx.adminx",
    # Your custom apps
    "app.main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
]

ROOT_URLCONF = "app.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.csp",
            ],
        },
    },
]

WSGI_APPLICATION = "app.config.wsgi.application"


# TailwindCSS

TAILWIND_CSS = {
    "config": APP_DIR / "config" / "tailwind.css",
}


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "assets/static/"

STATIC_ROOT = ASSETS_DIR / "static"


# Media files (User-uploaded content)
# https://docs.djangoproject.com/en/dev/ref/settings/#media-files

MEDIA_URL = "assets/media/"

MEDIA_ROOT = ASSETS_DIR / "media"


# Content Security Policy
# https://docs.djangoproject.com/en/dev/howto/csp/

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    # Example of the less secure 'unsafe-inline' option.
    # "style-src": [CSP.SELF, CSP.UNSAFE_INLINE],
}
