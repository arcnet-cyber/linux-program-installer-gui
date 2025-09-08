import subprocess
import os
from .base import PackageManager

class DnfManager(PackageManager):
    def search_package(self, name):
        env = os.environ.copy()
        env["LANG"] = "C"  # Ensure consistent English output

        result = subprocess.run(
            ["dnf", "search", name],
            capture_output=True,
            text=True,
            env=env
        )

        if result.returncode != 0:
            print("[!] dnf search failed:")
            print(result.stderr)
            return []

        lines = result.stdout.strip().splitlines()
        packages = []

        for line in lines:
            line = line.strip()

            # Skip metadata lines, empty lines, and DNF "Matched fields"
            if not line or line.startswith("Updating") or line.startswith("Repositories loaded") or line.startswith("Matched fields") or ":" not in line:
                continue

            # Format: package.arch: Description
            if ":" in line:
                pkg_part, desc = line.split(":", 1)
                pkg_name = pkg_part.strip().split(".")[0]  # Strip architecture
                packages.append((pkg_name, desc.strip()))

        return packages

    def validate_package(self, name):
        env = os.environ.copy()
        env["LANG"] = "C"

        result = subprocess.run(
            ["dnf", "info", name],
            capture_output=True,
            text=True,
            env=env
        )

        if result.returncode != 0:
            return False

        for line in result.stdout.splitlines():
            if line.strip().startswith("Name"):
                found_name = line.split(":", 1)[1].strip()
                return found_name == name
        return False

    def clean_package_list(self, package_list):
        seen = set()
        valid = []

        for pkg, desc in package_list:
            if pkg not in seen:
                seen.add(pkg)
                if self.validate_package(pkg):
                    valid.append((pkg, desc))
                else:
                    print(f"[!] Package not found or not installable: {pkg}")
        return valid

    def generate_install_command(self, packages):
        names = [pkg for pkg, _ in packages]
        return f"sudo dnf install -y {' '.join(names)}"

    # -------------------------
    # UNINSTALL SUPPORT METHODS
    # -------------------------

    def generate_uninstall_command(self, packages):
        names = [pkg for pkg, _ in packages]
        return f"sudo dnf remove -y {' '.join(names)}"

    def list_installed_packages(self):
        env = os.environ.copy()
        env["LANG"] = "C"

        # Correct command to list installed packages
        result = subprocess.run(
            ["dnf", "list", "--installed"],
            capture_output=True,
            text=True,
            env=env
        )

        packages = []
        lines = result.stdout.strip().splitlines()

        for line in lines:
            line = line.strip()
            # Skip header/metadata/error lines
            if not line or line.startswith("Installed Packages") or line.startswith("Last metadata") or line.startswith("Error:"):
                continue

            parts = line.split()
            if len(parts) >= 1:
                pkg_name = parts[0].split(".")[0]  # drop architecture
                packages.append((pkg_name, ""))

        return packages
