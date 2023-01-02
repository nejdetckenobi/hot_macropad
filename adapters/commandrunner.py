from adapters.base import ReleaseExecuteAction

import pynput
import os


class CommandRunner(ReleaseExecuteAction):
    def __init__(self, command):
        super(CommandRunner, self).__init__()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        os.system(self.command)
        super(CommandRunner, self).run(context=context)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)
