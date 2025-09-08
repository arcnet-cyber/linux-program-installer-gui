import subprocess
from .base import PackageManager

class ZypperManager(PackageManager):
    def search_package(self, name):
        result = subprocess.run(
            ["zypper", "search", "-s", name],
            capture_output=True,
            text=True
        )
        lines = result.stdout.strip().splitlines()

        packages = []
        parsing = False

        for line in lines:
            line = line.strip()
            # Detect the header row
            if "Name" in line and ("Repository" in line or "Summary" in line):
                parsing = True
                continue
            if not parsing or line.startswith("---") or not line:
                continue

            # Format: S | Name | Type | Version | Arch | Repository
            parts = [part.strip() for part in line.split("|")]
            if len(parts) >= 2:
                status = parts[0].lower() if parts[0] else "-"
                pkg_name = parts[1]

                if status.startswith("i"):
                    desc = "Installed"
                else:
                    desc = "Available"

                packages.append((pkg_name, desc))
        return packages

    def validate_package(self, name):
        result = subprocess.run(
            ["zypper", "info", name],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        # If package exists, output contains "Information for package <name>"
        return f"Information for package {name}" in output

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
        return f"sudo zypper install -y {' '.join(names)}"

    # -------------------------
    # UNINSTALL SUPPORT METHODS
    # -------------------------

    def generate_uninstall_command(self, packages):
        names = [pkg for pkg, _ in packages]
        return f"sudo zypper remove -y {' '.join(names)}"

    def list_installed_packages(self):
        result = subprocess.run(
            ["zypper", "search", "-i"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().splitlines()

        packages = []
        parsing = False

        for line in lines:
            line = line.strip()
            # Detect header row
            if "Name" in line and ("Repository" in line or "Summary" in line):
                parsing = True
                continue
            if not parsing or line.startswith("---") or not line:
                continue

            parts = [part.strip() for part in line.split("|")]
            if len(parts) >= 2:
                pkg_name = parts[1]
                packages.append((pkg_name, ""))  # description not available

        return packages
