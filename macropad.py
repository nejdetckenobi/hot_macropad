#!/usr/bin/env python

import json
from datetime import datetime
from threading import Thread

from evdev import InputDevice, categorize, ecodes
from adapters import get_adapter
from sys import argv, exit


class BaseMacropadDevice(object):
    def __init__(self, device_path):
        self.device = InputDevice(device_path)
        self.grab()

    def grab(self):
        self.device.grab()


class BaseMacroPadListener(BaseMacropadDevice):
    def echo(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key = categorize(event)
                if key.keystate == key.key_up:
                    print(key.keycode)


class BaseMacropadConfigurer(BaseMacropadDevice):
    def prepare_config_with_listen(self, file_path=None, page_count=1):
        keys = set()
        try:
            for event in self.device.read_loop():
                if event.type == ecodes.EV_KEY:
                    key = categorize(event)
                    if key.keystate == key.key_up:
                        keys.add(key.keycode)
        except KeyboardInterrupt:
            pass
        result = {"page{}".format(i): dict.fromkeys(sorted(keys)) for i in range(page_count)}
        if file_path is None:
            print("\n" + json.dumps(result, indent=4, ensure_ascii=False))
        else:
            with open(file_path, "w") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)


class BaseMacroPadRunner(BaseMacroPadListener):
    def __init__(self, device_path, locked=False, start_page_name=None):
        super(BaseMacroPadRunner, self).__init__(device_path)
        self.actions = {}
        self.context = {
            "actions": self.actions,
            "action_page_name": start_page_name,
            "hold_start": None,
            "hold_lock": False,
            "locked": locked,
        }

    def initialize_actions(self, action_pages_file):
        self.actions = self.get_action_map(action_pages_file)
        self.context["actions"] = self.actions

    @staticmethod
    def get_action_map(file_path):
        actions = {}

        with open(file_path) as f:
            data = json.load(f)

        for page_name, page_data in data.items():
            page = {}
            actions[page_name] = page
            for key_code, adapter_data in page_data.items():
                if adapter_data is None:
                    continue
                adapter_file, adapter_name = adapter_data.pop('adapter').rsplit('.', 1)
                adapter = get_adapter(adapter_file, adapter_name)
                page[key_code] = adapter(**adapter_data)
        return actions

    def main_loop(self):
        event_source = self.device.read_loop()
        while True:
            event = next(event_source)
            if event.type != ecodes.EV_KEY:
                continue
            key = categorize(event)

            action = self.actions.get(self.context["action_page_name"], {}).get(key.keycode)
            if key.keystate == key.key_down:
                self.context["hold_start"] = datetime.now()

                if self.context["locked"]:
                    pass
                elif action is None:
                    print("No action specified for", key.keycode,
                          "press in action page:", self.context["action_page_name"])
                else:
                    action.press(self.context)
            elif key.keystate == key.key_up:
                self.context["hold_start"] = None
                self.context["hold_lock"] = False

                if self.context["locked"]:
                    pass
                elif action is None:
                    print("No action specified for", key.keycode,
                          "release in action page:", self.context["action_page_name"])
                else:
                    action.release(self.context)
            elif key.keystate == key.key_hold:
                if action is not None:
                    action.hold(self.context)


class MacroPadListener(BaseMacroPadListener):
    pass


class MacroPadConfigurer(BaseMacropadConfigurer):
    pass


class MacroPadRunner(BaseMacroPadRunner):
    pass

