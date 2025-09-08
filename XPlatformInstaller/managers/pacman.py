import subprocess
from .base import PackageManager


class PacmanManager(PackageManager):
    def search_package(self, name):
        result = subprocess.run(
            ["pacman", "-Ss", name],
            capture_output=True,
            text=True
        )
        lines = result.stdout.strip().splitlines()

        packages = []
        current_name = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "/" in line and " " in line:
                # Example: community/gparted 1.5.0-1
                parts = line.split()
                repo_pkg = parts[0]
                if "/" in repo_pkg:
                    current_name = repo_pkg.split("/", 1)[1]  # safely extract package name
            elif current_name:
                # Example: "A graphical partition manager"
                description = line.strip()
                packages.append((current_name, description))
                current_name = ""

        return packages

    def validate_package(self, name):
        result = subprocess.run(
            ["pacman", "-Si", name],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        return "Name" in output and "Repository" in output

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
        return f"sudo pacman -S --noconfirm {' '.join(names)}"

    # -------------------------
    # UNINSTALL SUPPORT METHODS
    # -------------------------

    def generate_uninstall_command(self, packages):
        names = [pkg for pkg, _ in packages]
        return f"sudo pacman -R --noconfirm {' '.join(names)}"

    def list_installed_packages(self):
        result = subprocess.run(
            ["pacman", "-Q"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = []
        for line in result.stdout.splitlines():
            parts = line.split()
            pkg = parts[0]
            # pacman -Q does not provide description; leave empty
            packages.append((pkg, ""))
        return packages
