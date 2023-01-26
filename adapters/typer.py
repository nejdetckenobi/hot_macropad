import pynput

from adapters.base.mixins import ReleaseExecuteActionMixin, HoldExecuteActionMixin


class TyperMixin:
    def __init__(self, command):
        super(TyperMixin, self).__init__()
        self.kb_controller = pynput.keyboard.Controller()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        self.kb_controller.type(self.command)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__,
                                   self.command.strip())


class ReleaseTyper(ReleaseExecuteActionMixin, TyperMixin):
    def __init__(self, command):
        TyperMixin.__init__(self, command)
        ReleaseExecuteActionMixin.__init__(self)

    def run(self, context=None):
        return TyperMixin.run(self, context=context)


class HoldTyper(HoldExecuteActionMixin, TyperMixin):
    def __init__(self, command, deltaseconds):
        TyperMixin.__init__(self, command)
        HoldExecuteActionMixin.__init__(self, deltaseconds)

    def run(self, context=None):
        TyperMixin.run(self, context=context)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__,
                                   self.command.strip())
