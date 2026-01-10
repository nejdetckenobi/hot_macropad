#!/usr/bin/env bash

# evdev-like macropad event reader with script-driven page switching
# Usage: ./script.sh /dev/input/eventX [default_page]

set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 /dev/input/eventX [default_page]"
    exit 1
fi

DEVICE="$1"
DEFAULT_PAGE="${2:-default}"
CONFIG_BASE="${XDG_CONFIG_HOME:-$HOME/.config}"
# Optional config directory override (3rd argument)
CONFIG_DIR_OVERRIDE="${3:-}"
CONFIG_DIR="${CONFIG_DIR_OVERRIDE:-$CONFIG_BASE/hot_macropad}"
CURRENT_PAGE="$DEFAULT_PAGE"

if [[ ! -e "$DEVICE" ]]; then
    echo "Device not found: $DEVICE"
    exit 1
fi

if [[ ! -d "$CONFIG_DIR/$CURRENT_PAGE" ]]; then
    echo "Initial page not found: $CONFIG_DIR/$CURRENT_PAGE"
    exit 1
fi

if ! command -v evtest >/dev/null 2>&1; then
    echo "evtest is required but not installed"
    exit 1
fi

# Check scripts in the current page and warn if missing or not executable
shopt -s nullglob
scripts=($CONFIG_DIR/$CURRENT_PAGE/*.sh)
if [[ ${#scripts[@]} -eq 0 ]]; then
    echo "[WARN] No scripts found in page $CURRENT_PAGE"
fi

for script in "${scripts[@]}"; do
    [[ ! -x "$script" ]] && echo "[WARN] $script is not executable"
done

# Apply page change if script requests it
apply_page_change() {
    local output="$1"

    if [[ "$output" =~ ^PAGE=([a-zA-Z0-9_-]+)$ ]]; then
        local new_page="${BASH_REMATCH[1]}"

        if [[ -d "$CONFIG_DIR/$new_page" ]]; then
            CURRENT_PAGE="$new_page"
            echo "[PAGE] switched to $CURRENT_PAGE"
        else
            echo "[PAGE] requested page not found: $new_page"
        fi
    fi
}

# evtest output is parsed to extract key name and value
# Use stdbuf for line-buffered output so logs appear immediately
while read -r line; do
    [[ "$line" != *"EV_KEY"* ]] && continue

    key=$(echo "$line" | sed -n 's/.*code \([0-9]*\) (\(KEY_[A-Z0-9_]*\)).*/\2/p')
    value=$(echo "$line" | sed -n 's/.*value \([-0-9]*\).*/\1/p')

    [[ -z "$key" || -z "$value" ]] && continue

    case "$value" in
        0)
            # RELEASE
            script="$CONFIG_DIR/$CURRENT_PAGE/$key.sh"

            if [[ ! -e "$script" ]]; then
                echo "[WARN] $CURRENT_PAGE/$key script not found"
            elif [[ ! -x "$script" ]]; then
                echo "[WARN] $CURRENT_PAGE/$key script exists but is not executable"
            else
                echo "[RUN] $CURRENT_PAGE/$key"

                output=$("$script" 2>&1)
                echo "$output"

                apply_page_change "$output"
            fi
            ;;
    esac

done < <(stdbuf -oL evtest --grab "$DEVICE")
