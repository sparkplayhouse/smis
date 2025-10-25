"""
Django management command for managing Tailwind CSS.

Usage:
    python manage.py tailwind install [--force]
    python manage.py tailwind watch
    python manage.py tailwind build
    python manage.py tailwind status
"""

import platform
import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Manage Tailwind CSS installation and builds"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            dest="subcommand", help="Available subcommands", required=True
        )

        install_parser = subparsers.add_parser(
            "install", help="Install npm dependencies"
        )
        install_parser.add_argument(
            "--force",
            action="store_true",
            help="Force reinstall by removing node_modules first",
        )

        subparsers.add_parser(
            "watch", help="Run Tailwind CSS in development mode (minified with watch)"
        )

        subparsers.add_parser(
            "build", help="Build Tailwind CSS for production (minified)"
        )

        subparsers.add_parser("status", help="Check Tailwind CSS setup status")

    def handle(self, *args, **options):
        base_app_dir = Path(__file__).resolve().parent.parent.parent

        # Input directory - where the Tailwind config CSS file will be copied to
        # and where npm commands will be executed from
        self.tailwind_input_dir = base_app_dir / "static_src" / "tailwind"

        # Output file path - the complete path to the final compiled CSS file
        self.output_css_path = (
            base_app_dir / "static" / "djanx" / "base" / "tailwind" / "output.min.css"
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
        """Validate that the tailwind directory and package.json exist."""
        if not self.tailwind_input_dir.exists():
            raise CommandError(f"Directory does not exist: {self.tailwind_input_dir}")

        package_json = self.tailwind_input_dir / "package.json"
        if not package_json.exists():
            raise CommandError(f"package.json not found in {self.tailwind_input_dir}")

    def _validate_tailwind_config(self):
        """Validate that TAILWIND_CSS_CONFIG setting is configured and the file exists."""
        # Check if setting exists
        if not hasattr(settings, "TAILWIND_CSS_CONFIG"):
            raise CommandError(
                "TAILWIND_CSS_CONFIG setting is not defined in your Django settings.\n"
                "Please add it to your settings file, for example:\n"
                "TAILWIND_CSS_CONFIG = BASE_DIR / 'app' / 'conf' / 'tailwind.config.css'"
            )

        config_setting = settings.TAILWIND_CSS_CONFIG

        # Check if setting is a non-empty string or Path
        if not config_setting:
            raise CommandError(
                f"TAILWIND_CSS_CONFIG must be a non-empty string or Path, got: {config_setting!r}"
            )

        # Convert to Path object if it's a string
        if isinstance(config_setting, str):
            config_path = Path(config_setting)
        elif isinstance(config_setting, Path):
            config_path = config_setting
        else:
            raise CommandError(
                f"TAILWIND_CSS_CONFIG must be a string or Path object, got: {type(config_setting).__name__}"
            )

        # Check if directory / file exists
        if not config_path.exists():
            raise CommandError(
                f"Tailwind CSS config file not found: {config_path}\n"
                f"TAILWIND_CSS_CONFIG is set to: {config_setting}\n"
                "Please ensure the file exists or update the TAILWIND_CSS_CONFIG setting."
            )

        # Check if it's actually file (not a directory)
        if not config_path.is_file():
            raise CommandError(
                f"TAILWIND_CSS_CONFIG must point to a file, not a directory: {config_path}"
            )

        self.stdout.write(self.style.SUCCESS(f"✓ Using config: {config_path}"))

        return config_path

    def _copy_config_to_tailwind_dir(self, source_config):
        """Copy the config file to tailwind directory for Tailwind CSS v4."""
        dest_config = self.tailwind_input_dir / "input.css"

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
        node_modules = self.tailwind_input_dir / "node_modules"
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
            node_modules = self.tailwind_input_dir / "node_modules"
            if node_modules.exists():
                self.stdout.write("Removing existing node_modules...")
                shutil.rmtree(node_modules)

        self.stdout.write(
            f"Installing npm dependencies in {self.tailwind_input_dir}..."
        )

        try:
            result = subprocess.run(
                [self.npm_command, "install"],
                cwd=self.tailwind_input_dir,
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
        source_config = self._validate_tailwind_config()
        self._check_npx()
        self._ensure_node_modules()
        local_config = self._copy_config_to_tailwind_dir(source_config)

        self.stdout.write("Starting Tailwind CSS in watch mode...")
        self.stdout.write(f"Output: {self.output_css_path}")
        self.stdout.write("Press Ctrl+C to stop")

        try:
            subprocess.run(
                [
                    self.npx_command,
                    "@tailwindcss/cli",
                    "-i",
                    str(local_config.name),
                    "-o",
                    str(self.output_css_path),
                    "--minify",
                    "--watch",
                ],
                cwd=self.tailwind_input_dir,
                check=True,
            )
        except KeyboardInterrupt:
            self.stdout.write("\nStopped Tailwind CSS watch mode")
        except subprocess.CalledProcessError:
            raise CommandError("Tailwind CSS watch failed")

    def build(self):
        """Build Tailwind CSS for production."""
        self._validate_setup()
        source_config = self._validate_tailwind_config()
        self._check_npx()
        self._ensure_node_modules()
        local_config = self._copy_config_to_tailwind_dir(source_config)

        self.stdout.write("Building Tailwind CSS for production...")
        self.stdout.write(f"Output: {self.output_css_path}")

        try:
            result = subprocess.run(
                [
                    self.npx_command,
                    "@tailwindcss/cli",
                    "-i",
                    str(local_config.name),
                    "-o",
                    str(self.output_css_path),
                    "--minify",
                ],
                cwd=self.tailwind_input_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            self.stdout.write(self.style.SUCCESS("✓ Tailwind CSS build completed"))

            if self.output_css_path.exists():
                size = self.output_css_path.stat().st_size / 1024
                self.stdout.write(
                    f"Output file: {self.output_css_path} ({size:.2f} KB)"
                )

            if result.stdout:
                self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR("✗ Build failed"))
            self.stdout.write(e.stderr)
            raise CommandError("Tailwind CSS build failed")

    def status(self):
        """Check Tailwind CSS setup status."""
        self.stdout.write(self.style.MIGRATE_HEADING("djanX Tailwind CSS Setup Status"))
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

        # Validate Tailwind CSS config setting and file existence
        try:
            self._validate_tailwind_config()
        except CommandError as e:
            self.stdout.write(self.style.ERROR("✗ TAILWIND_CSS_CONFIG issue:"))
            self.stdout.write(f"  {str(e)}")

        # Check if the compiled output CSS file exists
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
                    f"⚠ Output CSS not found: {self.output_css_path}\n"
                    "  (run: python manage.py tailwind [watch / build])"
                )
            )
