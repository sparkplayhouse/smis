from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir or file'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Tailwind CSS configuration file path
TAILWIND_CSS_CONFIG = BASE_DIR / "app" / "conf" / "tailwind.config.css"


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
]

ROOT_URLCONF = "app.conf.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "app.conf.wsgi.application"


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
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
#
# Media files (User-uploaded content)
# https://docs.djangoproject.com/en/dev/ref/settings/#media-files

ASSETS_DIR = BASE_DIR / "app" / "assets"

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

# Static files configuration
STATIC_URL = "app/assets/static/"
STATIC_ROOT = ASSETS_DIR / "static"

# Media files configuration
MEDIA_URL = "app/assets/media/"
MEDIA_ROOT = ASSETS_DIR / "media"
