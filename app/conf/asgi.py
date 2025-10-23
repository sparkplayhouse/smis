"""
ASGI config.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Unlike manage.py, asgi.py uses production settings by default.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.conf.production")

application = get_asgi_application()
