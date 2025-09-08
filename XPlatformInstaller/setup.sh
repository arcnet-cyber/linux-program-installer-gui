#!/usr/bin/env bash

set -e

# 1. Detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

OS_ID=$(detect_os)
echo "Detected OS: $OS_ID"

# 2. Confirm Python 3 install
read -rp "Do you want to install Python 3 and dependencies? (y/n): " INSTALL_PYTHON
INSTALL_PYTHON=${INSTALL_PYTHON,,} # to lowercase

if [[ "$INSTALL_PYTHON" == "y" ]]; then
    echo "Installing Python 3, pip, and Tkinter..."

    case "$OS_ID" in
        arch|manjaro|arcolinux|endeavouros|garuda)
            sudo pacman -Sy --noconfirm python python-pip tk
            ;;
        void)
            sudo xbps-install -Sy python3 python3-pip tk
            ;;
        debian|ubuntu|linuxmint|pop|elementary|kali|zorin|neon|parrot|trisquel)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-tk
            ;;
        fedora|rhel|centos|almalinux|rocky|ol|oracle)
            sudo dnf install -y python3 python3-pip python3-tkinter
            ;;
        opensuse|suse|opensuse-leap|opensuse-tumbleweed|sles)
            sudo zypper install -y python3 python3-pip python3-tk
            ;;
        *)
            echo "Unsupported OS: $OS_ID"
            exit 1
            ;;
    esac

    echo "Python 3, pip, and Tkinter installed."
else
    echo "Skipping Python 3 installation."
fi

# 3. Create 'installer' alias/function
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL_ENTRY="$SCRIPT_DIR/main.py"

if [ ! -f "$TOOL_ENTRY" ]; then
    echo "Could not find main.py in: $SCRIPT_DIR"
    exit 1
fi

# Determine user's shell
USER_SHELL=$(basename "$SHELL")

case "$USER_SHELL" in
    bash)
        SHELL_RC="$HOME/.bashrc"
        ALIAS_CMD="alias installer='python3 \"$TOOL_ENTRY\"'"
        if ! grep -Fxq "$ALIAS_CMD" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"            # Add blank line
            echo "$ALIAS_CMD" >> "$SHELL_RC"
            echo "Alias 'installer' added to $SHELL_RC"
        else
            echo "Alias 'installer' already exists in $SHELL_RC"
        fi
        ;;
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ALIAS_CMD="alias installer='sudo python3 \"$TOOL_ENTRY\"'"
        if ! grep -Fxq "$ALIAS_CMD" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"            # Add blank line
            echo "$ALIAS_CMD" >> "$SHELL_RC"
            echo "Alias 'installer' added to $SHELL_RC"
        else
            echo "Alias 'installer' already exists in $SHELL_RC"
        fi
        ;;
    fish)
        FISH_CONFIG="$HOME/.config/fish/config.fish"
        FISH_FUNC="function installer\n    python3 \"$TOOL_ENTRY\"\nend"
        if ! grep -Fq "function installer" "$FISH_CONFIG"; then
            echo -e "\n$FISH_FUNC" >> "$FISH_CONFIG"
            echo "Function 'installer' added to $FISH_CONFIG"
        else
            echo "Function 'installer' already exists in $FISH_CONFIG"
        fi
        ;;
    *)
        echo "Unsupported shell: $USER_SHELL"
        echo "Please manually add an alias or function to your shell config file."
        ;;
esac

# 4. Final Instructions
echo
echo "Setup complete!"
echo "Reboot your terminal"
echo "Then run your tool with:"
echo "installer"
