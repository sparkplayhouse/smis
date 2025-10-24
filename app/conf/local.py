from pathlib import Path
from split_settings.tools import include

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-f+nixt7zjkqi9l*ju5(kpv$e!+f@01b_b(#90rbzjpr0e&vr-i"

ALLOWED_HOSTS = []

# Include settings segments
SPLIT = Path(__file__).parent / "settings"

include(
    str(SPLIT / "main.py"),  # Load main settings first
    str(SPLIT / "assets.py"),
)
