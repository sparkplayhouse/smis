"""
Django management command for managing TailwindCSS.

Usage:
    python manage.py tailwindcss install
    python manage.py tailwindcss build
    python manage.py tailwindcss status
"""

import platform
import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Manage TailwindCSS installation and builds"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            dest="subcommand", help="Available subcommands", required=True
        )

        # install subcommand
        install_parser = subparsers.add_parser(
            "install",
            help="Install tailwindcss node dependencies. Requires nodejs/npm is installed.",
        )
        install_parser.add_argument(
            "--force",
            action="store_true",
            help="Force reinstall by removing node_modules before installation.",
        )

        # build subcommand
        subparsers.add_parser("build", help="Build TailwindCSS (minified)")

        # status subcommand
        subparsers.add_parser("status", help="Check TailwindCSS setup status")

    def handle(self, *args, **options):
        tailwindcss_dir = Path(__file__).resolve().parent.parent.parent

        # Where the Tailwind config CSS file will be copied to
        # and where npm commands will be executed from
        self.management_dir = tailwindcss_dir / "management"

        # Output file path - the complete path to the final compiled CSS file
        self.output_css_path = tailwindcss_dir / "static" / "tailwindcss" / "min.css"

        self.tailwindcss_settings = getattr(settings, "TAILWIND_CSS", {})

        subcommand = options["subcommand"]

        match subcommand:
            case "install":
                self.install(force=options["force"])
            case "build":
                self.build()
            case "status":
                self.status()

    def _validate_setting(self):
        """Validate that TAILWIND_CSS setting is configured and the file exists."""
        if not self.tailwindcss_settings or "config" not in self.tailwindcss_settings:
            raise CommandError(
                (
                    "TAILWIND_CSS setting with a 'config' key is not defined in your Django settings.\n"
                    "Please add it to your settings file, for example:\n"
                    "TAILWIND_CSS = {\n"
                    "    'config': APP_DIR / 'config' / 'tailwind.css',\n"
                    "}"
                )
            )

        config_setting = self.tailwindcss_settings["config"]

        # Check if setting is a non-empty string or Path
        if not config_setting:
            raise CommandError(
                f"TAILWIND_CSS['config'] must be a non-empty string or Path, got: {config_setting!r}"
            )

        # Convert to Path object if it's a string
        if isinstance(config_setting, str):
            config_path = Path(config_setting)
        elif isinstance(config_setting, Path):
            config_path = config_setting
        else:
            raise CommandError(
                f"TAILWIND_CSS['config'] must be a string or Path object, got: {type(config_setting).__name__}"
            )

        # Check if directory / file exists
        if not config_path.exists():
            raise CommandError(
                (
                    f"TailwindCSS config file not found: {config_path}\n"
                    f"TAILWIND_CSS['config'] is set to: {config_setting}\n"
                    "Please ensure the file exists or update the TAILWIND_CSS setting."
                )
            )

        # Check if it's actually file (not a directory)
        if not config_path.is_file():
            raise CommandError(
                f"TAILWIND_CSS['config'] must point to a file, not a directory: {config_path}"
            )

        self.stdout.write(self.style.SUCCESS(f"✓ Using config: {config_path}"))

        return config_path

    def _copy_config(self, source_config):
        """Copy the tailwindcss config file to management directory."""
        dest_config = self.management_dir / "config.css"

        try:
            # Check if source and destination are the same file
            if source_config.resolve() == dest_config.resolve():
                # Already in the right place, no need to copy
                return dest_config

            shutil.copy2(source_config, dest_config)
            return dest_config
        except Exception as e:
            raise CommandError(f"Failed to copy config file: {e}")

    def _get_npm_command(self):
        return shutil.which("npm")

    def _get_npx_command(self):
        return shutil.which("npx")

    def _check_npm(self):
        """Check if npm is available and store the command."""
        npm_command = self._get_npm_command()

        if not npm_command:
            raise CommandError(
                (
                    "npm not found in PATH. Please ensure Node.js and npm are installed "
                    "and added to your system PATH.\n"
                    "Visit: https://nodejs.org/\n\n"
                    "After installation, you may need to:\n"
                    "  - Restart your terminal/IDE\n"
                    "  - Add npm to your PATH environment variable\n"
                    f"  - Current OS: {platform.system()}"
                )
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
                (
                    "npx not found in PATH. Please ensure Node.js and npm are installed "
                    "and added to your system PATH.\n"
                    "Visit: https://nodejs.org/\n\n"
                    "After installation, you may need to:\n"
                    "  - Restart your terminal/IDE\n"
                    "  - Add npx to your PATH environment variable\n"
                    f"  - Current OS: {platform.system()}"
                )
            )

        self.npx_command = npx_command

        # Verify it works
        try:
            subprocess.run([npx_command, "--version"], capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            raise CommandError(
                f"npx found at '{npx_command}' but failed to execute.\nError: {str(e)}"
            )

    def _ensure_node_modules(self, force=False):
        """Ensure node_modules exists, install if not."""
        node_modules = self.management_dir / "node_modules"
        if not node_modules.exists() or force:
            self.install(force=force)

    def install(self, force=False):
        """Install tailwindcss dependencies."""
        self._check_npm()

        node_modules = self.management_dir / "node_modules"

        if force and node_modules.exists():
            self.stdout.write("Force option used. Removing node dependecies...")
            try:
                shutil.rmtree(node_modules)
                self.stdout.write(self.style.SUCCESS("✓ Removed node_modules"))
            except Exception as e:
                raise CommandError(f"Failed to remove node_modules: {e}")

        self.stdout.write("Installing node dependencies...")

        try:
            result = subprocess.run(
                [self.npm_command, "install"],
                cwd=self.management_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            self.stdout.write(
                self.style.SUCCESS("✓ tailwindcss install completed successfully")
            )

            if result.stdout:
                self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR("✗ tailwindcss install failed"))
            self.stdout.write(e.stderr)
            raise CommandError("tailwindcss install failed")

    def build(self):
        """Build TailwindCSS"""
        source_config = self._validate_setting()
        self._check_npx()
        self._ensure_node_modules()
        local_config = self._copy_config(source_config)

        self.stdout.write("Building TailwindCSS...")

        try:
            command = [
                self.npx_command,
                "@tailwindcss/cli",
                "-i",
                str(local_config.name),
                "-o",
                str(self.output_css_path),
                "--minify",
            ]

            result = subprocess.run(
                command,
                cwd=self.management_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            self.stdout.write(self.style.SUCCESS("✓ TailwindCSS build completed"))

            if self.output_css_path.exists():
                size = self.output_css_path.stat().st_size / 1024
                self.stdout.write(f"Build size: {size:.2f} KB")

            if result.stdout:
                self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR("✗ Build failed"))
            self.stdout.write(e.stderr)
            raise CommandError("TailwindCSS build failed")

    def status(self):
        """Check TailwindCSS setup status."""
        self.stdout.write(self.style.MIGRATE_HEADING("djanX TailwindCSS Setup Status"))
        self.stdout.write("-" * 50)

        # Check if npm is available and get its version
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

        # Check if npx is available and get its version
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

        # Validate TailwindCSS config setting and file existence
        config_valid = True
        try:
            self._validate_setting()
        except CommandError as e:
            config_valid = False
            self.stdout.write(self.style.ERROR("✗ TAILWIND_CSS issue:"))
            self.stdout.write(f"  {str(e)}")

        # Check if the compiled output CSS file exists
        # Only check for output file if config validation passed
        if config_valid:
            if self.output_css_path.exists():
                size = self.output_css_path.stat().st_size / 1024
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Output CSS: {self.output_css_path} ({size:.2f} KB)"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "⚠ Output CSS not found\n(run: python manage.py tailwindcss build)"
                    )
                )
