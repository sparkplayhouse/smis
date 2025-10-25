from pathlib import Path
from split_settings.tools import include

DEBUG = True

SECRET_KEY = "django-insecure-f+nixt7zjkqi9l*ju5(kpv$e!+f@01b_b(#90rbzjpr0e&vr-i"

ALLOWED_HOSTS = []

# Include main settings

include(str(Path(__file__).resolve().parent / "settings.py"))
