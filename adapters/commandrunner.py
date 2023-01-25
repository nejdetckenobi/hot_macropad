from adapters.base.mixins import (ReleaseExecuteActionMixin,
                                  HoldExecuteActionMixin)

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
        super(CommandRunnerMixin, self).run(context=context)


class CommandRunner(ReleaseExecuteActionMixin, CommandRunnerMixin):
    def __init__(self, command):
        CommandRunnerMixin.__init__(self, command)
        ReleaseExecuteActionMixin.__init__(self)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)


class HoldCommandRunner(HoldExecuteActionMixin, CommandRunnerMixin):
    def __init__(self, command, deltaseconds):
        CommandRunnerMixin.__init__(self, command)
        HoldExecuteActionMixin.__init__(self, deltaseconds)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)

