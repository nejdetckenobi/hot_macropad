import pynput

from adapters.base.mixins import (ReleaseAction,
                                  HoldAction)


class Typer:
    def __init__(self, command):
        super(Typer, self).__init__()
        self.kb_controller = pynput.keyboard.Controller()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        self.kb_controller.type(self.command)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__,
                                   self.command.strip())


class ReleaseTyper(ReleaseAction, Typer):
    def __init__(self, command):
        Typer.__init__(self, command)
        ReleaseAction.__init__(self)

    def run(self, context=None):
        return Typer.run(self, context=context)


class ReleaseFileTyper(ReleaseTyper):
    def run(self, context=None):
        if context["locked"]:
            return
        with open(self.command) as f:
            data = f.read()

        self.kb_controller.type(data)


class HoldTyper(HoldAction, Typer):
    def __init__(self, command, deltaseconds):
        Typer.__init__(self, command)
        HoldAction.__init__(self, deltaseconds)

    def run(self, context=None):
        Typer.run(self, context=context)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__,
                                   self.command.strip())
