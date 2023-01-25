from adapters.base import HoldExecuteActionMixin


class PadLocker(HoldExecuteActionMixin):
    def __init__(self, *args, **kwargs):
        super(PadLocker, self).__init__(*args, **kwargs)
        self.state = None

    def run(self, context=None):
        context["locked"] = not context["locked"]
        self.state = context["locked"]
        return super(PadLocker, self).run(context)

    def __repr__(self):
        return "{}(locked={})".format(self.__class__.__name__, self.state)
