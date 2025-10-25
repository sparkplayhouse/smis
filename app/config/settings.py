from pathlib import Path

from django.utils.csp import CSP

# Build paths inside the project like this: BASE_DIR / 'subdir or file'.

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = BASE_DIR / "app"

# Tailwind CSS configuration file path

TAILWIND_CONFIG_CSS = APP_DIR / "config" / "tailwind.css"


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "djanx.adminx",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djanx.base",
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


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================
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


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

ASSETS_DIR = APP_DIR / "assets"

# Ensure assets directory exists

ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Create a .gitignore file in the assets directory to ignore its contents

gitignore_path = ASSETS_DIR / ".gitignore"
if not gitignore_path.exists():
    gitignore_path.write_text(
        "# * Automatically generated once (unless you delete the entire assets folder)\n"
        "# * As it's generated once, it will not be overwritten - you can safely edit it\n"
        "\n"
        "# Ignore all files within this directory\n"
        "*"
    )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "assets/static/"

STATIC_ROOT = ASSETS_DIR / "static"

# Media files (User-uploaded content)
# https://docs.djangoproject.com/en/dev/ref/settings/#media-files

MEDIA_URL = "assets/media/"

MEDIA_ROOT = ASSETS_DIR / "media"


# ==============================================================================
# CONTENT SECURITY POLICY (CSP) SETTINGS
# ==============================================================================
# https://docs.djangoproject.com/en/dev/howto/csp/

SECURE_CSP = {
    "default-src": [CSP.SELF],
    # Allow self-hosted scripts and script tags with matching `nonce` attr.
    "script-src": [CSP.SELF, CSP.NONCE],
    # Example of the less secure 'unsafe-inline' option.
    "style-src": [CSP.SELF, CSP.UNSAFE_INLINE],
}
