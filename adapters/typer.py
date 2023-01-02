import pynput

from adapters.base import ReleaseExecuteAction


class Typer(ReleaseExecuteAction):
    def __init__(self, command):
        super(Typer, self).__init__()
        self.kb_controller = pynput.keyboard.Controller()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        self.kb_controller.type(self.command)
        super(Typer, self).run(context=context)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)
