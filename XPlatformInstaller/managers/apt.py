import subprocess
from .base import PackageManager


class AptManager(PackageManager):
    def search_package(self, name):
        result = subprocess.run(
            ["apt-cache", "search", name],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()

        # Extract only package names and descriptions
        packages = []
        for line in lines:
            if " - " in line:
                pkg, desc = line.split(" - ", 1)
                packages.append((pkg.strip(), desc.strip()))

        return packages  # list of tuples (name, description)

    def validate_package(self, name):
        result = subprocess.run(
            ["apt-cache", "policy", name],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()

        # A valid installable package should have a non-'none' candidate
        for line in output.splitlines():
            if line.strip().startswith("Candidate:"):
                return "none" not in line
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
        return f"sudo apt install -y {' '.join(names)}"

    # -------------------------
    # UNINSTALL SUPPORT METHODS
    # -------------------------

    def generate_uninstall_command(self, packages):
        names = [pkg for pkg, _ in packages]
        return f"sudo apt remove -y {' '.join(names)}"

    def list_installed_packages(self):
        result = subprocess.run(
            ["apt", "list", "--installed"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = []
        for line in result.stdout.splitlines():
            if line and not line.startswith("Listing..."):
                if "/" in line and "installed" in line:
                    pkg = line.split("/")[0]
                    # apt list does not give description; leave empty
                    packages.append((pkg, ""))
        return packages
