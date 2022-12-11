from adapters.base import ReleaseExecuteAction
import pynput


class RelativeCommandRunner(ReleaseExecuteAction):
    def __init__(self, command):
        super(RelativeCommandRunner, self).__init__()
        self.kb_controller = pynput.keyboard.Controller()
        self.command = command

    def run(self, context=None):
        if context["locked"]:
            return
        self.kb_controller.type(self.command + "\r")
        super(RelativeCommandRunner, self).run(context=context)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.command)
