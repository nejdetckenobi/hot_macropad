from datetime import datetime, timedelta


class BaseAction(object):

    def press(self, context=None):
        pass

    def release(self, context=None):
        pass

    def hold(self, context=None):
        pass

    def run(self, context=None):
        print(self)

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)


class PressExecuteAction(BaseAction):
    def press(self, context=None):
        return self.run(context=context)


class ReleaseExecuteAction(BaseAction):
    def release(self, context=None):
        return self.run(context=context)


class HoldExecuteAction(BaseAction):
    def __init__(self, deltaseconds):
        super(HoldExecuteAction, self).__init__()
        self.deltaseconds = timedelta(seconds=deltaseconds)

    def hold(self, context=None):
        if context["hold_lock"]:
            return

        now = datetime.now()
        if context["hold_start"] + self.deltaseconds < now:
            context["hold_lock"] = True
            context["hold_start"] = None
            self.run(context=context)
