"""See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/"""

from pathlib import Path
from decouple import config, Csv
from split_settings.tools import include

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config("SECRET_KEY")

# Allowed hosts in production

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# Include main settings

include(str(Path(__file__).resolve().parent / "settings.py"))
