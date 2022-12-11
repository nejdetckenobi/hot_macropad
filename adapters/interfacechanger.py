from adapters.base import ReleaseExecuteAction


class InterfaceChanger(ReleaseExecuteAction):
    def __init__(self):
        super(InterfaceChanger, self).__init__()
        self.content = ""

    def run(self, context=None):
        if context["locked"]:
            return
        c = context
        c["interface_no"] = (c["interface_no"] + 1) % c["action_page_count"]
        self.content = c["interface_no"]
        super(InterfaceChanger, self).run(context=context)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.content)
