from .pacman import PacmanManager
from .xbps import XbpsManager
from .apt import AptManager
from .dnf import DnfManager
from .zypper import ZypperManager

def get_manager(os_id):
    os_id = os_id.lower()

    # Arch-based distros
    if os_id in ("arch", "manjaro", "arcolinux", "endeavouros", "garuda"):
        return PacmanManager()

    # Void
    elif os_id == "void":
        return XbpsManager()

    # Debian-based distros
    elif os_id in (
        "debian", "ubuntu", "linuxmint", "pop", "elementary", "zorin", "kali",
        "parrot", "neon", "peppermint", "lxle", "bodhi", "deepin", "trisquel",
        "ubuntu-mate", "xubuntu", "lubuntu", "ubuntu-budgie", "mx"
    ):
        return AptManager()

    # Red Hat-based distros
    elif os_id in (
        "fedora", "rhel", "centos", "almalinux", "rocky", "ol", "oracle"
    ):
        return DnfManager()

    # openSUSE-based
    elif os_id in (
        "opensuse", "opensuse-leap", "opensuse-tumbleweed", "suse", "sles"
    ):
        return ZypperManager()

    else:
        raise NotImplementedError(f"No package manager implemented for OS: {os_id}")
