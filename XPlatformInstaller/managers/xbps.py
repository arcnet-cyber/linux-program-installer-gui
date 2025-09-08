import subprocess
from .base import PackageManager

class XbpsManager(PackageManager):
    def search_package(self, name):
        result = subprocess.run(
            ["xbps-query", "-Rs", name],
            capture_output=True,
            text=True
        )
        lines = result.stdout.strip().splitlines()
        packages = []

        for line in lines:
            s = line.strip()
            if not s:
                continue

            # Remove leading status token like "[-]" or "[I]"
            if s.startswith("["):
                rb = s.find("]")
                if rb != -1:
                    s = s[rb+1:].lstrip()

            # First token is repo/package-version
            first, rest = (s.split(None, 1) + [""])[:2]

            # Remove repo prefix
            pkg_full = first.split("/", 1)[-1]  # e.g., "thc-hydra-9.4_1"

            # Remove version for menu display
            if "-" in pkg_full:
                pkg_name = "-".join(pkg_full.split("-")[:-1])
            else:
                pkg_name = pkg_full

            desc = rest.strip()
            packages.append((pkg_name, desc))

        return packages

    def validate_package(self, name):
        """
        Skip validation — trust the search results.
        """
        return True  # always valid for Void

    def clean_package_list(self, package_list):
        """
        Deduplicate only, do not validate.
        """
        seen = set()
        valid = []
        for pkg, desc in package_list:
            if pkg not in seen:
                seen.add(pkg)
                valid.append((pkg, desc))
        return valid

    def generate_install_command(self, packages):
        """
        Return a string for use with subprocess.run(shell=True)
        """
        names = [pkg for pkg, _ in packages]
        return f"sudo xbps-install -Sy {' '.join(names)}"

    # -------------------------
    # UNINSTALL SUPPORT METHODS
    # -------------------------

    def generate_uninstall_command(self, packages):
        names = [pkg for pkg, _ in packages]
        return f"sudo xbps-remove -Ry {' '.join(names)}"

    def list_installed_packages(self):
        result = subprocess.run(
            ["xbps-query", "-l"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = []
        for line in result.stdout.splitlines():
            s = line.strip()
            if not s:
                continue

            # Format: status pkg-version
            parts = s.split()
            if len(parts) < 2:
                continue
            pkg_full = parts[1]

            # Remove version for menu display
            if "-" in pkg_full:
                pkg_name = "-".join(pkg_full.split("-")[:-1])
            else:
                pkg_name = pkg_full

            packages.append((pkg_name, ""))  # no description
        return packages
