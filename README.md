# Hot Macropad

Hot Macropad is a user-level macropad daemon for Linux. It allows you to assign scripts to keys to perform macros and switch pages.

---

## 1. Installation

### Requirements

* Bash
* evtest
* xdotool (optional, for macros)

### Installation Steps

1. Copy the script to a directory in your PATH and make it executable:

```bash
mkdir -p ~/bin
cp hot-macropad.sh ~/bin/hot-macropad
chmod +x ~/bin/hot-macropad
```

2. Create the config directory and add example scripts:

```bash
mkdir -p ~/.config/hot_macropad/default
# Example script
echo -e "#!/usr/bin/env bash\necho 'KEY_A pressed'" > ~/.config/hot_macropad/default/KEY_A.sh
chmod +x ~/.config/hot_macropad/default/KEY_A.sh
```

3. Add your user to the `input` group (no sudo required when running after this):

```bash
sudo usermod -aG input $USER
# To apply without logout:
newgrp input
```

4. Install the user service for systemd:

```bash
mkdir -p ~/.config/systemd/user
cp hot-macropad.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable hot-macropad.service
systemctl --user start hot-macropad.service
```

> Note: Adjust the device path in `ExecStart` of `hot-macropad.service` to match your macropad.

---

## 2. Usage

### Startup

* Default page: `default`
* To start with a different page:

```bash
~/bin/hot-macropad /dev/input/eventX page1
```

### Script Structure

* One script per key (`KEY_A.sh`, `KEY_B.sh`, etc.)
* Executed on key release
* Script stdout and stderr are printed to terminal
* To request a page switch from a script, output a single line:

```bash
PAGE=page1
```

* Config directory structure:

```
~/.config/hot_macropad/
 ├─ default/
 │   ├─ KEY_A.sh
 │   └─ ...
 ├─ page1/
 └─ page2/
```

### Example Script

`~/.config/hot_macropad/default/KEY_F13.sh`:

```bash
#!/usr/bin/env bash
# This script switches to page1
echo "PAGE=page1"
```

---

## 3. Viewing Logs

To view user service logs:

```bash
journalctl --user -u hot-macropad.service -f
```

Script outputs and page switch messages appear here.

---

With this setup, you can use multiple macropads, assign scripts to each key, and run the daemon at the user level without needing sudo.

