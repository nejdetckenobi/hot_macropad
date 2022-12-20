from adapters.base import ReleaseExecuteAction

import pynput
import os


class GlobalCommandRunner(ReleaseExecuteAction):
    def __init__(self, command):
        super(GlobalCommandRunner, self).__init__()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        os.system(self.command)
        super(GlobalCommandRunner, self).run(context=context)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)


class CommandPasteAndReturn(ReleaseExecuteAction):
    def __init__(self, command):
        super(CommandPasteAndReturn, self).__init__()
        self.kb_controller = pynput.keyboard.Controller()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        self.kb_controller.type(self.command + "\r")
        super(CommandPasteAndReturn, self).run(context=context)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)
