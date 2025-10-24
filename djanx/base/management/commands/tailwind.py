"""
Django management command for managing Tailwind CSS.

Usage:
    python manage.py tailwind install [--force]
    python manage.py tailwind dev
    python manage.py tailwind build
    python manage.py tailwind status
"""

import subprocess
import shutil
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Manage Tailwind CSS installation and builds"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            dest="subcommand", help="Available subcommands", required=True
        )

        # Install subcommand
        install_parser = subparsers.add_parser(
            "install", help="Install npm dependencies"
        )
        install_parser.add_argument(
            "--force",
            action="store_true",
            help="Force reinstall by removing node_modules first",
        )

        # Dev subcommand
        subparsers.add_parser(
            "dev", help="Run Tailwind CSS in development mode (with watch)"
        )

        # Build subcommand
        subparsers.add_parser(
            "build", help="Build Tailwind CSS for production (minified)"
        )

        # Status subcommand
        subparsers.add_parser("status", help="Check npm setup status")

    def handle(self, *args, **options):
        self.tailwind_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "static"
            / "djanx"
            / "base"
            / "tailwind"
        )

        subcommand = options["subcommand"]

        match subcommand:
            case "install":
                self.install(options.get("force", False))
            case "dev":
                self.dev()
            case "build":
                self.build()
            case "status":
                self.status()

    def _validate_setup(self):
        """Validate that the base directory and package.json exist."""
        if not self.tailwind_dir.exists():
            raise CommandError(f"Directory does not exist: {self.tailwind_dir}")

        package_json = self.tailwind_dir / "package.json"
        if not package_json.exists():
            raise CommandError(f"package.json not found in {self.tailwind_dir}")

    def _check_npm(self):
        """Check if npm is available."""
        try:
            subprocess.run(["npm", "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            raise CommandError(
                "npm not found. Please install Node.js and npm first.\n"
                "Visit: https://nodejs.org/"
            )

    def _ensure_node_modules(self):
        """Ensure node_modules exists, install if not."""
        node_modules = self.tailwind_dir / "node_modules"
        if not node_modules.exists():
            self.stdout.write(
                self.style.WARNING(
                    "node_modules not found. Running npm install first..."
                )
            )
            self.install(force=False)

    def install(self, force=False):
        """Install npm dependencies."""
        self._validate_setup()
        self._check_npm()

        # Remove node_modules if --force flag is used
        if force:
            node_modules = self.tailwind_dir / "node_modules"
            if node_modules.exists():
                self.stdout.write("Removing existing node_modules...")
                shutil.rmtree(node_modules)

        self.stdout.write(f"Installing npm dependencies in {self.tailwind_dir}...")

        try:
            result = subprocess.run(
                ["npm", "install"],
                cwd=self.tailwind_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            self.stdout.write(
                self.style.SUCCESS("✓ npm install completed successfully")
            )

            if result.stdout:
                self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR("✗ npm install failed"))
            self.stdout.write(e.stderr)
            raise CommandError("npm install failed")

    def dev(self):
        """Run Tailwind CSS in development/watch mode."""
        self._validate_setup()
        self._check_npm()
        self._ensure_node_modules()

        self.stdout.write("Starting Tailwind CSS in watch mode...")
        self.stdout.write("Press Ctrl+C to stop")

        try:
            subprocess.run(["npm", "run", "dev"], cwd=self.tailwind_dir, check=True)
        except KeyboardInterrupt:
            self.stdout.write("\nStopped Tailwind CSS watch mode")
        except subprocess.CalledProcessError:
            raise CommandError("npm run dev failed")

    def build(self):
        """Build Tailwind CSS for production."""
        self._validate_setup()
        self._check_npm()
        self._ensure_node_modules()

        self.stdout.write("Building Tailwind CSS for production...")

        try:
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=self.tailwind_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            self.stdout.write(self.style.SUCCESS("✓ Tailwind CSS build completed"))

            # Check if output file was created
            output_css = self.tailwind_dir / "output" / "tailwind.css"
            if output_css.exists():
                size = output_css.stat().st_size / 1024  # Size in KB
                self.stdout.write(f"Output file: {output_css} ({size:.2f} KB)")

            if result.stdout:
                self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR("✗ Build failed"))
            self.stdout.write(e.stderr)
            raise CommandError("npm run build failed")

    def status(self):
        """Check Tailwind CSS setup status."""
        self.stdout.write(self.style.MIGRATE_HEADING("Tailwind CSS Setup Status"))
        self.stdout.write("-" * 50)

        # Check base directory
        if self.tailwind_dir.exists():
            self.stdout.write(
                self.style.SUCCESS(f"✓ Base directory: {self.tailwind_dir}")
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"✗ Base directory not found: {self.tailwind_dir}")
            )
            return

        # Check package.json
        package_json = self.tailwind_dir / "package.json"
        if package_json.exists():
            self.stdout.write(self.style.SUCCESS("✓ package.json found"))
            with open(package_json, "r") as f:
                data = json.load(f)
                self.stdout.write(f"  Name: {data.get('name', 'N/A')}")
        else:
            self.stdout.write(self.style.ERROR("✗ package.json not found"))

        # Check node_modules
        node_modules = self.tailwind_dir / "node_modules"
        if node_modules.exists():
            num_packages = len(list(node_modules.iterdir()))
            self.stdout.write(
                self.style.SUCCESS(f"✓ node_modules exists ({num_packages} items)")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "⚠ node_modules not found (run: python manage.py tailwind install)"
                )
            )

        # Check output directory
        output_css = self.tailwind_dir / "output.css"
        if output_css.exists():
            size = output_css.stat().st_size / 1024
            self.stdout.write(
                self.style.SUCCESS(f"✓ Output CSS exists ({size:.2f} KB)")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "⚠ Output CSS not found (run: python manage.py tailwind build)"
                )
            )

        # Check npm availability
        try:
            result = subprocess.run(
                ["npm", "--version"], capture_output=True, text=True, check=True
            )
            self.stdout.write(
                self.style.SUCCESS(f"✓ npm version: {result.stdout.strip()}")
            )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("✗ npm not found in PATH"))
