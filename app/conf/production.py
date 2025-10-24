"""See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/"""

from pathlib import Path
from decouple import config, Csv
from split_settings.tools import include, optional

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# Include settings segments
SPLIT = Path(__file__).parent / "settings"

include(
    str(SPLIT / "main.py"),  # Load main settings first
    str(SPLIT / "assets.py"),
)
