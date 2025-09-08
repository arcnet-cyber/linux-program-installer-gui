#!/usr/bin/env bash

set -e

ALIAS_NAME="installer"
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"
FISHRC="$HOME/.config/fish/config.fish"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)/linux-program-installer"

remove_alias() {
    local file=$1
    if [ -f "$file" ] && grep -q "alias $ALIAS_NAME=" "$file"; then
        echo "Removing alias '$ALIAS_NAME' from $file..."
        sed -i "/alias $ALIAS_NAME=/d" "$file"
        echo "Alias removed."
    else
        echo "No alias '$ALIAS_NAME' found in $file."
    fi
}

# 1. Remove aliases from supported shells
remove_alias "$BASHRC"
remove_alias "$ZSHRC"

# Fish uses a different syntax
if [ -f "$FISHRC" ] && grep -q "alias $ALIAS_NAME " "$FISHRC"; then
    echo "Removing alias '$ALIAS_NAME' from $FISHRC..."
    sed -i "/alias $ALIAS_NAME /d" "$FISHRC"
    echo "Alias removed."
else
    echo "No alias '$ALIAS_NAME' found in $FISHRC."
fi

# 2. Ask if they want to delete the project folder
read -rp "Do you want to delete the project directory at $TARGET_DIR? (y/n): " DELETE_PROJECT
DELETE_PROJECT=${DELETE_PROJECT,,} # convert to lowercase

if [[ "$DELETE_PROJECT" == "y" ]]; then
    read -rp "Are you sure? This will permanently delete: $TARGET_DIR (y/n): " CONFIRM_DELETE
    CONFIRM_DELETE=${CONFIRM_DELETE,,}

    if [[ "$CONFIRM_DELETE" == "y" ]]; then
        rm -rf "$TARGET_DIR"
        echo "Project directory deleted."
    else
        echo "Project deletion cancelled."
    fi
else
    echo "Project files retained."
fi

# 3. Final note
echo
echo "Uninstall complete!"