from adapters.base.mixins import ReleaseAction

from pynput.mouse import Controller, Button
from threading import Thread, Event
from time import sleep


class AutoClicker(ReleaseAction):

    def __init__(self, button="left", interval=0.03):
        ReleaseAction.__init__(self)
        self.stop_event = Event()
        self.interval = interval
        self.mouse_controler = Controller()
        self.button_name = button
        self.thread = None

    @property
    def button(self):
        return getattr(Button, self.button_name)

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.button_name)

    def _clicker(self):
        while not self.stop_event.is_set():
            self.mouse_controler.click(self.button)
            sleep(self.interval)

    def run(self, context: dict | None = None):
        state = context.get("autoclick_active", False)
        if not state:
            self.stop_event = Event()
            self.thread = Thread(target=self._clicker, daemon=True)
            self.thread.start()
            context["autoclick_active"] = True
        else:
            self.stop_event.set()
            context["autoclick_active"] = False
        super(AutoClicker, self).run(context=context)
