from .settings import *  # noqa: F403

DEBUG = True

SECRET_KEY = "django-insecure-f+nixt7zjkqi9l*ju5(kpv$e!+f@01b_b(#90rbzjpr0e&vr-i"

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "thespark",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
