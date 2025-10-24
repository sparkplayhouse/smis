"""
Django management command for managing Tailwind CSS.

Usage:
    python manage.py tailwind install [--force]
    python manage.py tailwind watch
    python manage.py tailwind build
    python manage.py tailwind status
"""

import json
import platform
import shutil
import subprocess
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
            "watch", help="Run Tailwind CSS in development mode (with watch)"
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
            case "watch":
                self.watch()
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

    def _get_npm_command(self):
        """
        Find and return the npm command.

        Returns the full path to npm if found in PATH, otherwise None.
        Users should ensure npm is in their system PATH.
        """
        return shutil.which("npm")

    def _get_npx_command(self):
        """
        Find and return the npx command.

        Returns the full path to npx if found in PATH, otherwise None.
        Users should ensure npx is in their system PATH.
        """
        return shutil.which("npx")

    def _check_npm(self):
        """Check if npm is available and store the command."""
        npm_command = self._get_npm_command()

        if not npm_command:
            raise CommandError(
                "npm not found in PATH. Please ensure Node.js and npm are installed "
                "and added to your system PATH.\n"
                "Visit: https://nodejs.org/\n\n"
                "After installation, you may need to:\n"
                "  - Restart your terminal/IDE\n"
                "  - Add npm to your PATH environment variable\n"
                f"  - Current OS: {platform.system()}"
            )

        self.npm_command = npm_command

        # Verify it works
        try:
            subprocess.run([npm_command, "--version"], capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            raise CommandError(
                f"npm found at '{npm_command}' but failed to execute.\nError: {str(e)}"
            )

    def _check_npx(self):
        """Check if npx is available and store the command."""
        npx_command = self._get_npx_command()

        if not npx_command:
            raise CommandError(
                "npx not found in PATH. Please ensure Node.js and npm are installed "
                "and added to your system PATH.\n"
                "Visit: https://nodejs.org/\n\n"
                "After installation, you may need to:\n"
                "  - Restart your terminal/IDE\n"
                "  - Add npx to your PATH environment variable\n"
                f"  - Current OS: {platform.system()}"
            )

        self.npx_command = npx_command

        # Verify it works
        try:
            subprocess.run([npx_command, "--version"], capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            raise CommandError(
                f"npx found at '{npx_command}' but failed to execute.\nError: {str(e)}"
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
                [self.npm_command, "install"],
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

    def watch(self):
        """Run Tailwind CSS in development/watch mode."""
        self._validate_setup()
        self._check_npx()
        self._ensure_node_modules()

        self.stdout.write("Starting Tailwind CSS in watch mode...")
        self.stdout.write("Press Ctrl+C to stop")

        try:
            subprocess.run(
                [
                    self.npx_command,
                    "@tailwindcss/cli",
                    "-i",
                    "./input.css",
                    "-o",
                    "./output.css",
                    "--watch",
                ],
                cwd=self.tailwind_dir,
                check=True,
            )
        except KeyboardInterrupt:
            self.stdout.write("\nStopped Tailwind CSS watch mode")
        except subprocess.CalledProcessError:
            raise CommandError("Tailwind CSS watch failed")

    def build(self):
        """Build Tailwind CSS for production."""
        self._validate_setup()
        self._check_npx()
        self._ensure_node_modules()

        self.stdout.write("Building Tailwind CSS for production...")

        try:
            result = subprocess.run(
                [
                    self.npx_command,
                    "@tailwindcss/cli",
                    "-i",
                    "./input.css",
                    "-o",
                    "./output.css",
                    "--minify",
                ],
                cwd=self.tailwind_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            self.stdout.write(self.style.SUCCESS("✓ Tailwind CSS build completed"))

            # Check if output file was created
            output_css = self.tailwind_dir / "output.css"
            if output_css.exists():
                size = output_css.stat().st_size / 1024  # Size in KB
                self.stdout.write(f"Output file: {output_css} ({size:.2f} KB)")

            if result.stdout:
                self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR("✗ Build failed"))
            self.stdout.write(e.stderr)
            raise CommandError("Tailwind CSS build failed")

    def status(self):
        """Check Tailwind CSS setup status."""
        self.stdout.write(self.style.MIGRATE_HEADING("DjanX Tailwind CSS Setup Status"))
        self.stdout.write("-" * 50)

        # Check tailwind directory
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

        # Check npm availability
        npm_command = self._get_npm_command()
        if npm_command:
            try:
                result = subprocess.run(
                    [npm_command, "--version"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ npm version: {result.stdout.strip()} (at {npm_command})"
                    )
                )
            except subprocess.CalledProcessError:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠ npm found at {npm_command} but failed to execute"
                    )
                )
        else:
            self.stdout.write(
                self.style.ERROR(f"✗ npm not found in PATH (OS: {platform.system()})")
            )

        # Check npx availability
        npx_command = self._get_npx_command()
        if npx_command:
            try:
                result = subprocess.run(
                    [npx_command, "--version"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ npx version: {result.stdout.strip()} (at {npx_command})"
                    )
                )
            except subprocess.CalledProcessError:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠ npx found at {npx_command} but failed to execute"
                    )
                )
        else:
            self.stdout.write(
                self.style.ERROR(f"✗ npx not found in PATH (OS: {platform.system()})")
            )

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

        # Check output css
        output_css = self.tailwind_dir / "output.css"
        if output_css.exists():
            size = output_css.stat().st_size / 1024
            self.stdout.write(
                self.style.SUCCESS(f"✓ Output CSS exists ({size:.2f} KB)")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "⚠ Output CSS not found (run: python manage.py tailwind [watch / build])"
                )
            )
