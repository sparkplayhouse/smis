# Directory used to store project assets (static + media)
ASSETS_DIR = BASE_DIR / "app" / "assets"

# Ensure the assets directory exists when settings are imported
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
