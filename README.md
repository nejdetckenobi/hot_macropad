# Hot Macropad

Hot Macropad is a user-level macropad daemon for Linux.
It listens to input events from a macropad device and executes user-defined scripts per key, with optional page switching.

---

## Installation

### Install via Deb Package

Install the downloaded `.deb` package:

```
sudo dpkg -i hot-macropad_0.1.0-1_amd64.deb
```

If dependency errors occur:

```
sudo apt -f install
```

This will:

* Install the `hot-macropad` script to `/usr/bin/hot-macropad`
* Install the systemd **user** unit template

---

### Manual Installation (from Source)

Clone the repository:

```
git clone https://github.com/nejdetckenobi/hot_macropad.git
cd hot_macropad
```

Install the script into your PATH:

```
mkdir -p ~/bin
cp hot-macropad.sh ~/bin/hot-macropad
chmod +x ~/bin/hot-macropad
```

Install the systemd user unit file:

```
mkdir -p ~/.config/systemd/user
cp hot-macropad@.service ~/.config/systemd/user/
systemctl --user daemon-reload
```

---

## Config Directory Structure

Default config directory:

```
~/.config/hot_macropad/
```

Example layout:

```
~/.config/hot_macropad/
 ├─ default/
 │   ├─ KEY_A.sh
 │   ├─ KEY_B.sh
 │   └─ KEY_F13.sh
 ├─ page1/
 └─ page2/
```

Create the default page:

```
mkdir -p ~/.config/hot_macropad/default
```

Rules:

* One script per key
* Script name must match the key code (e.g. `KEY_A.sh`)
* Scripts must be executable

---

## systemd Usage After Installation

### Recommended Method (by-id)

List available input devices:

```
ls /dev/input/by-id/
```

Example device name:

```
usb-MYINPUTDEVICE-event-kbd
```

Enable and start the service:

```
systemctl --user enable hot-macropad@usb-MYINPUTDEVICE-event-kbd.service
systemctl --user start  hot-macropad@usb-MYINPUTDEVICE-event-kbd.service
```

View logs:

```
journalctl --user -u hot-macropad@usb-MYINPUTDEVICE-event-kbd.service -f
```

---

## Writing a Key Script (Example)

Example: show a desktop notification when `KEY_A` is released.

File:

```
~/.config/hot_macropad/default/KEY_A.sh
```

Contents:

```
#!/usr/bin/env bash
notify-send "Hot Macropad" "KEY_A pressed"
```

Make it executable:

```
chmod +x ~/.config/hot_macropad/default/KEY_A.sh
```

---

## eventX Fallback

Some devices may not appear under `/dev/input/by-id/`
(common with certain Bluetooth or virtual devices).

In this case, override the systemd unit.

### Create an Override

```
systemctl --user edit hot-macropad@my-device.service
```

Add:

```
[Service]
ExecStart=
ExecStart=/usr/bin/hot-macropad /dev/input/event12
```

Then enable and start:

```
systemctl --user enable hot-macropad@my-device.service
systemctl --user start  hot-macropad@my-device.service
```

> Note: `eventX` numbers may change between reboots.
> This method should only be used if `by-id` is unavailable.


## Versioning
Git tags and Debian package versions are identical.
Every released .deb corresponds to a Git tag with the exact same version string.
