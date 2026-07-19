# Hot Macropad

Hot Macropad is a user-level macropad daemon for Linux.
It listens to input events from a macropad device and executes user-defined scripts per key, with optional page switching.

---

## Installation

### Install via Deb Package

Install the downloaded `.deb` package:

```
sudo dpkg -i hot-macropad_0.2.0_all.deb
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

Enable and start the service (the plain instance name is retained for
compatibility with `/dev/input/by-id/` entries):

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

## Devices Without a by-id Entry

Some devices may not appear under `/dev/input/by-id/`
(common with certain Bluetooth or virtual devices).

Because `eventX` numbers may change between reboots, create a persistent,
uniquely named device alias with a udev rule instead of relying on a specific
`eventX` path. Use a different alias for every macropad.

### Create a Persistent udev Alias

First, identify the current event device and inspect its attributes:

```
udevadm info --attribute-walk --name=/dev/input/event12
```

Find attributes that uniquely identify the device, such as `idVendor` and
`idProduct`. Then create `/etc/udev/rules.d/99-hot-macropad.rules`. In this
example, `editing-pad` is the custom name chosen for the device:

```udev
SUBSYSTEM=="input", KERNEL=="event*", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", ENV{ID_INPUT_KEYBOARD}=="1", SYMLINK+="input/editing-pad"
```

Replace `1234` and `5678` with the values reported for your device. If more
than one connected device has the same vendor and product IDs, add its serial
number to the same rule to distinguish it:

```udev
SUBSYSTEM=="input", KERNEL=="event*", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", ATTRS{serial}=="DEVICE_SERIAL_NUMBER", ENV{ID_INPUT_KEYBOARD}=="1", SYMLINK+="input/editing-pad"
```

Additional devices can have their own rules and names, for example
`input/streaming-pad`.

Reload the rules and reconnect the device:

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Verify that the alias exists:

```
ls -l /dev/input/editing-pad
```

### Use the Alias in the Service

Convert the full alias path to a systemd instance name:

```
systemd-escape --path /dev/input/editing-pad
```

This prints `dev-input-editing\x2dpad`. Use that value to enable and start the
service:

```bash
systemctl --user enable --now 'hot-macropad@dev-input-editing\x2dpad.service'
```

Repeat these steps with a unique alias and service instance for each device.

### Direct eventX Fallback

For temporary use or troubleshooting, an `eventX` path can also be converted
to a service instance:

```
systemd-escape --path /dev/input/event12
systemctl --user start hot-macropad@dev-input-event12.service
```

> Note: `eventX` numbers may change between reboots.
> Prefer `/dev/input/by-id/` or a persistent udev alias for normal use.


## Versioning
Git tags and Debian package versions are identical.
Every released .deb corresponds to a Git tag with the exact same version string.
