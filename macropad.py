#!/usr/bin/env python

import json
from datetime import datetime
from evdev import InputDevice, categorize, ecodes
from adapters import get_adapter
from sys import argv, exit


class MacroPad(object):
    def __init__(self, device_path, locked=False):
        super(MacroPad, self).__init__()
        self.actions = []
        self.device = InputDevice(device_path)
        self.grab()
        self.context = {
            "interface_no": 0,
            "action_page_count": len(self.actions),
            "hold_start": None,
            "hold_lock": False,
            "locked": locked,
        }

    def initialize_actions(self, action_pages_file):
        self.actions = self.get_action_map(action_pages_file)
        self.context["action_page_count"] = len(self.actions)

    def grab(self):
        self.device.grab()

    @staticmethod
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
                adapter_file, adapter_name = adapter_data.pop('adapter').rsplit('.', 1)
                adapter = get_adapter(adapter_file, adapter_name)
                page[key_code] = adapter(**adapter_data)
        return actions

    def main_loop(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key = categorize(event)

                action = self.actions[self.context["interface_no"]].get(key.keycode)
                if key.keystate == key.key_down:
                    self.context["hold_start"] = datetime.now()

                    if self.context["locked"]:
                        pass
                    elif action is None:
                        print("No press action specified:", key.keycode)
                    else:
                        action.press(self.context)
                elif key.keystate == key.key_up:
                    self.context["hold_start"] = None
                    self.context["hold_lock"] = False

                    if self.context["locked"]:
                        pass
                    elif action is None:
                        print("No release action specified:", key.keycode)
                    else:
                        action.release(self.context)
                elif key.keystate == key.key_hold:
                    if action is not None:
                        action.hold(self.context)

    def echo(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key = categorize(event)
                if key.keystate == key.key_up:
                    print(key.keycode)

    def prepare_config_with_listen(self, file_path=None):
        keys = set()
        try:
            for event in self.device.read_loop():
                if event.type == ecodes.EV_KEY:
                    key = categorize(event)
                    if key.keystate == key.key_up:
                        keys.add(key.keycode)
        except KeyboardInterrupt:
            pass
        result = [dict.fromkeys(sorted(keys))]
        if file_path is None:
            print(json.dumps(result, indent=4, ensure_ascii=False))
        else:
            with open(file_path, "w") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

