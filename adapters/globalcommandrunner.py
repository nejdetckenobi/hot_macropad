from adapters.base import ReleaseExecuteAction
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
