from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

TAILWIND_CSS_CONFIG = BASE_DIR / "tailwind.config.css"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "djanx.adminx",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djanx.base",
    "app.home",
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

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# Assets Directory (Static + Media)
ASSETS_DIR = BASE_DIR / "app" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Create a .gitignore file in the assets directory to ignore its contents
gitignore_path = ASSETS_DIR / ".gitignore"
if not gitignore_path.exists():
    gitignore_path.write_text(
        "# Automatically generated (once)\n"
        "# This file will not be overwritten - you can safely edit it\n"
        "# Ignore all files within this directory\n"
        "*\n"
    )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = "app/assets/static/"
STATIC_ROOT = ASSETS_DIR / "static"

# Media Files (User-uploaded content)
# https://docs.djangoproject.com/en/stable/ref/settings/#media-files
MEDIA_URL = "app/assets/media/"
MEDIA_ROOT = ASSETS_DIR / "media"
