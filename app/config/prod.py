"""See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/"""

from decouple import Csv, config

from .settings import *  # noqa: F403

# ! SECURITY WARNING: don't run with debug turned on in production

DEBUG = False

# ! SECURITY WARNING: keep the secret key used in production secret

SECRET_KEY = config("SECRET_KEY")

# ! SECURITY WARNING: be intentional about the specific domains/IPs where your app is hosted in production

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
