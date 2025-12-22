from adapters.base import BaseAction
from adapters.base.mixins import ReleaseAction, HoldAction

import os


class BaseCommandRunner(BaseAction):
    def __init__(self, command):
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        super(BaseCommandRunner, self).run(context=context)
        os.system(self.command)

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.command)


class CommandRunner(ReleaseAction, BaseCommandRunner):
    def __init__(self, command):
        BaseCommandRunner.__init__(self, command)


class HoldCommandRunner(HoldAction, BaseCommandRunner):
    def __init__(self, command, deltaseconds):
        CommandRunner.__init__(self, command)
        HoldAction.__init__(self, deltaseconds)

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.command)


class ToggleCommandRunner(ReleaseAction):
    def __init__(self, command1, command2):
        self.command1 = command1
        self.command2 = command2
        self.state = True

    def __repr__(self):
        if self.state:
            return '{}("{}")'.format(self.__class__.__name__, self.command1)
        else:
            return '{}("{}")'.format(self.__class__.__name__, self.command2)

    def run(self, context=None):
        if context["locked"]:
            return

        command = self.command1 if self.state else self.command2
        os.system(command)
        super(ToggleCommandRunner, self).run(context=context)
        self.state = not self.state
