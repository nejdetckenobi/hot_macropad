#!/usr/bin/env python
import json
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
from adapters import get_adapter
from sys import argv, exit


if len(argv) == 1:
    exit()

ACTION_PAGES_FILE = 'action_pages.json'


def get_action_map(file_path):
    actions = []

    with open(file_path) as f:
        data = json.load(f)

    for page_data in data:
        page = {}
        actions.append(page)
        for key_code, adapter_data in page_data.items():
            if adapter_data is None:
                continue
            adapter_name = adapter_data.pop('adapter')
            adapter = get_adapter(adapter_name)
            page[key_code] = adapter(**adapter_data)
    return actions


dev = InputDevice(argv[1])
dev.grab()


action_map = get_action_map(ACTION_PAGES_FILE)


context = {
    "interface_no": 0,
    "action_page_count": len(action_map),
    "hold_start": None,
    "hold_lock": False,
    "locked": False,
}


for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key = categorize(event)

        action = action_map[context["interface_no"]].get(key.keycode)
        if key.keystate == key.key_down:
            context["hold_start"] = datetime.now()

            if context["locked"]:
                pass
            elif action is None:
                print("No press action specified:", key.keycode)
            else:
                action.press(context)
        elif key.keystate == key.key_up:
            context["hold_start"] = None
            context["hold_lock"] = None

            if context["locked"]:
                pass
            elif action is None:
                print("No release action specified:", key.keycode)
            else:
                action.release(context)
        elif key.keystate == key.key_hold:
            if action is not None:
                action.hold(context)
