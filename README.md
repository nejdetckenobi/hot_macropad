# Hot Macropad

Hot Macropad is a Linux utility for managing custom macro pads. It allows users to bind scripts to keys and switch between multiple pages of macros. The tool captures key events from your macropad exclusively and executes scripts in response, without sending keypresses to the system.

## Features

* Exclusive capture of macropad keys using `evdev`.
* Script-driven macros on key release.
* Multiple pages/layers of macros.
* Page switching controlled via script output (`PAGE=<name>`).
* Configurable per-user setup using `~/.config/hot_macropad`.
* Fully foreground execution; macro scripts block until completion.
* Compatible with multiple macropads on the same system.

## Installation

1. Clone or copy the repository.
2. Copy the main script to a bin directory in your PATH:

   ```bash
   mkdir -p ~/bin
   cp hot-macropad.sh ~/bin/hot-macropad
   chmod +x ~/bin/hot-macropad
   ```
3. Create the configuration directory:

   ```bash
   mkdir -p ~/.config/hot_macropad/default
   ```
4. Add macro scripts to `~/.config/hot_macropad/default/` or other pages.

   * Scripts must be executable (`chmod +x script.sh`).
   * Script names should match key names (`KEY_A.sh`, `KEY_B.sh`, etc.).

## Usage

```bash
# Run with default page
hot-macropad /dev/input/eventX

# Run with a specific starting page
hot-macropad /dev/input/eventX page1
```

### Macro Scripts

* Scripts are executed **on key release**.
* Output can include page change commands:

  ```bash
  PAGE=page1
  ```
* Example script (`KEY_A.sh`):

  ```bash
  #!/usr/bin/env bash
  notify-send 'Key A pressed'
  PAGE=page1
  ```

## Configuration Directory Structure

```
~/.config/hot_macropad/
 ├─ default/
 │   ├─ KEY_A.sh
 │   ├─ KEY_B.sh
 ├─ page1/
 │   └─ KEY_A.sh
 └─ page2/
     └─ KEY_A.sh
```

* Each directory represents a page/layer.
* Scripts should be named after the key codes they correspond to.

## Systemd User Service

To run Hot Macropad automatically on login:

1. Copy the unit file:

   ```bash
   mkdir -p ~/.config/systemd/user
   cp hot-macropad.service ~/.config/systemd/user/
   ```
2. Reload user units and enable the service:

   ```bash
   systemctl --user daemon-reload
   systemctl --user enable hot-macropad.service
   systemctl --user start hot-macropad.service
   ```
3. Check logs:

   ```bash
   journalctl --user -u hot-macropad.service -f
   ```

## Requirements

* `bash`
* `evtest`
* `xdotool` (optional, if used in macros)
* Linux with evdev support

## Notes

* Hot Macropad **does not send key events to the system**. Grabbed keys are exclusive to the script.
* Multiple macropads are supported; run a separate instance for each device.
* The default page is `default`. You can specify a different starting page as the second argument.
* Scripts should be executable and produce optional output for page switching.

## License

MIT License

