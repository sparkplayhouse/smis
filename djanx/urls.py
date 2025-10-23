from django.apps import apps
from django.urls import path, include

urlpatterns = []

# Dynamically include paths for installed djanx apps
djanx_apps = {
    "djanx.base": "djanx.base.urls",
}

for app_name, url_module in djanx_apps.items():
    if apps.is_installed(app_name):
        # Extract the last part of app_name for the URL prefix
        app_prefix = app_name.split(".")[-1]
        urlpatterns.append(path(f"{app_prefix}/", include(url_module)))
