from adapters.base import (ReleaseExecuteAction,
                           HoldExecuteAction)

import pynput
import os


class CommandRunnerMixin:
    def __init__(self, command):
        super(CommandRunnerMixin, self).__init__()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        os.system(self.command)
        super(CommandRunner, self).run(context=context)



class CommandRunner(ReleaseExecuteAction, CommandRunnerMixin):
    def __init__(self, command):
        CommandRunnerMixin.__init__(self, command)
        ReleaseExecuteAction.__init__(self)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)


class HoldCommandRunner(HoldExecuteAction, CommandRunnerMixin):
    def __init__(self, command):
        CommandRunnerMixin.__init__(self, command)
        HoldExecuteAction.__init__(self)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)

