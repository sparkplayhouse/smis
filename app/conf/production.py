from pathlib import Path
from decouple import config
from split_settings.tools import include, optional

# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# Include settings segments
SPLIT = Path(__file__).parent / "settings"

include(
    str(SPLIT / "main.py"),  # Load main settings first
    str(SPLIT / "assets.py"),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "www.thesparkplayhouse.info"]
