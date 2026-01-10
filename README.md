# Hot Macropad

Hot Macropad is a minimal, script-driven macropad daemon for Linux built on top of evtest.
It allows mapping keys to executable scripts and switching between pages dynamically.

The project intentionally avoids abstractions, configuration formats, or frameworks.
What runs is always visible as shell scripts.

------------------------------------------------------------

FEATURES

- evdev-level input handling via evtest --grab
- One script per key
- Page-based configuration
- Script-driven page switching
- Multiple macropads supported via systemd template units
- User-level service (no sudo at runtime)

------------------------------------------------------------

REQUIREMENTS

- Bash (>= 4)
- evtest
- xdotool (optional, for macros)

------------------------------------------------------------

INSTALLATION

1. Install the script

    mkdir -p ~/bin
    cp hot-macropad.sh ~/bin/hot-macropad
    chmod +x ~/bin/hot-macropad

Ensure ~/bin is in your PATH.

------------------------------------------------------------

2. Permissions

Add your user to the input group to access /dev/input/event* devices:

    sudo usermod -aG input $USER
    newgrp input

------------------------------------------------------------

3. Configuration directory

Default config directory:

    $XDG_CONFIG_HOME/hot_macropad

Create initial setup:

    mkdir -p ~/.config/hot_macropad/default

Example key script:

    cat > ~/.config/hot_macropad/default/KEY_A.sh << 'EOF'
    #!/usr/bin/env bash
    echo "KEY_A released"
    EOF

    chmod +x ~/.config/hot_macropad/default/KEY_A.sh

------------------------------------------------------------

USAGE

Command-line usage:

    hot-macropad <device> [default_page] [config_dir]

Examples:

    hot-macropad /dev/input/event10
    hot-macropad /dev/input/event10 page1
    hot-macropad /dev/input/event10 default ~/.config/hot_macropad_left
    hot-macropad /dev/input/event11 default ~/.config/hot_macropad_right

------------------------------------------------------------

SCRIPT BEHAVIOR

- One script per key (KEY_A.sh, KEY_B.sh, ...)
- Scripts are executed on key release
- Script stdout and stderr are logged
- Missing or non-executable scripts are logged as warnings

------------------------------------------------------------

PAGE SWITCHING

A script may request a page switch by printing:

    PAGE=page_name

Example:

    #!/usr/bin/env bash
    echo "PAGE=page1"

If the page exists, Hot Macropad switches immediately.

------------------------------------------------------------

CONFIGURATION LAYOUT

    hot_macropad/
     ├─ default/
     │   ├─ KEY_A.sh
     │   ├─ KEY_B.sh
     ├─ page1/
     │   └─ KEY_A.sh
     └─ page2/

------------------------------------------------------------

SYSTEMD (USER SERVICE)

A systemd template unit is provided.

Install the unit:

    mkdir -p ~/.config/systemd/user
    cp systemd/hot-macropad@.service ~/.config/systemd/user/
    systemctl --user daemon-reload

Enable for a device:

    systemctl --user enable hot-macropad@event10.service
    systemctl --user start hot-macropad@event10.service

In the template unit, %i refers to the device name under /dev/input
(e.g. event10 -> /dev/input/event10)

------------------------------------------------------------

LOGS

View logs with:

    journalctl --user -u hot-macropad@event10.service -f

All script output, warnings, and page switch messages appear here.

------------------------------------------------------------

DESIGN PHILOSOPHY

- No configuration formats (JSON/YAML/TOML)
- No hidden state
- No magic device detection
- Scripts are the API
- Errors are visible and verbose

If something runs, you can open it and read it.

------------------------------------------------------------

LICENSE

MIT License

