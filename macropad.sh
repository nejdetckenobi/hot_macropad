#!/usr/bin/env bash

# evdev-like macropad event reader with script-driven page switching
# Usage: ./script.sh /dev/input/eventX [default_page]

set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 /dev/input/eventX [default_page]" >&2
    exit 1
fi

DEVICE="$1"
DEFAULT_PAGE="${2:-default}"
CONFIG_DIR="$HOME/.config/hot_macropad"
CURRENT_PAGE="$DEFAULT_PAGE"

if [[ ! -e "$DEVICE" ]]; then
    echo "Device not found: $DEVICE" >&2
    exit 1
fi

if [[ ! -d "$CONFIG_DIR/$CURRENT_PAGE" ]]; then
    echo "Initial page not found: $CONFIG_DIR/$CURRENT_PAGE" >&2
    exit 1
fi

if ! command -v evtest >/dev/null 2>&1; then
    echo "evtest is required but not installed" >&2
    exit 1
fi

# Apply page change if script requests it
apply_page_change() {
    local output="$1"

    if [[ "$output" =~ ^PAGE=([a-zA-Z0-9_-]+)$ ]]; then
        local new_page="${BASH_REMATCH[1]}"

        if [[ -d "$CONFIG_DIR/$new_page" ]]; then
            CURRENT_PAGE="$new_page"
            echo "[PAGE] switched to $CURRENT_PAGE"
        else
            echo "[PAGE] requested page not found: $new_page" >&2
        fi
    fi
}

# evtest output is parsed to extract key name and value
# Example line:
# Event: time 1700000000.123456, type 1 (EV_KEY), code 30 (KEY_A), value 1

evtest --grab "$DEVICE" | while read -r line; do
    [[ "$line" != *"EV_KEY"* ]] && continue

    key=$(echo "$line" | sed -n 's/.*code \([0-9]*\) (\(KEY_[A-Z0-9_]*\)).*/\2/p')
    value=$(echo "$line" | sed -n 's/.*value \([-0-9]*\).*/\1/p')

    [[ -z "$key" || -z "$value" ]] && continue

    case "$value" in
        0)
            # RELEASE
            script="$CONFIG_DIR/$CURRENT_PAGE/$key.sh"

            if [[ -x "$script" ]]; then
                echo "[RUN] $CURRENT_PAGE/$key"

                # Capture script output for page switch commands
                output=$("$script" 2>&1)
                echo "$output"

                apply_page_change "$output"
            fi
            ;;
    esac

done

