from datetime import timedelta, datetime

from adapters.base import BaseAction


class LockableAction(BaseAction):
    def run(self, context=None):
        if not context["locked"]:
            super(LockableAction, self).run(context=context)


class PressAction(BaseAction):
    def press(self, context=None):
        return self.run(context=context)


class ReleaseAction(BaseAction):
    def release(self, context=None):
        return self.run(context=context)


class HoldAction(BaseAction):
    def __init__(self, deltaseconds):
        self.deltaseconds = timedelta(seconds=deltaseconds)

    def hold(self, context=None):
        if context["hold_lock"]:
            return

        now = datetime.now()
        if context["hold_start"] + self.deltaseconds < now:
            context["hold_lock"] = True
            context["hold_start"] = None
            self.run(context=context)
