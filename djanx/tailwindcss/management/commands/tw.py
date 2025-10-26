"""
Shorter alias for the tailwindcss management command.

Usage:
    python manage.py tw install
    python manage.py tw build
    python manage.py tw status
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from .tailwindcss import add_tailwindcss_arguments


class Command(BaseCommand):
    help = "Shortcut for 'tailwindcss' command - Manage TailwindCSS installation and builds"

    def add_arguments(self, parser):
        add_tailwindcss_arguments(parser)

    def handle(self, *args, **options):
        # Extract subcommand and forward to tailwindcss command
        subcommand = options.pop("subcommand")
        call_command("tailwindcss", subcommand, **options)
