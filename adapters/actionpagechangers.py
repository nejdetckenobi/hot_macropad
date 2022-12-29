from adapters.base import ReleaseExecuteAction


class NextActionPage(ReleaseExecuteAction):
    def __init__(self):
        super(NextActionPage, self).__init__()
        self.content = ""

    def run(self, context=None):
        if context["locked"]:
            return
        c = context
        c["interface_no"] = (c["interface_no"] + 1) % c["action_page_count"]
        self.content = c["interface_no"]
        super(NextActionPage, self).run(context=context)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.content)


class PreviousActionPage(ReleaseExecuteAction):
    def __init__(self):
        super(PreviousActionPage, self).__init__()
        self.content = ""

    def run(self, context=None):
        if context["locked"]:
            return
        c = context
        c["interface_no"] = (c["interface_no"] - 1) % c["action_page_count"]
        self.content = c["interface_no"]
        super(PreviousActionPage, self).run(context=context)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.content)


class ActionPageSetter(ReleaseExecuteAction):
    def __init__(self, page_number):
        super(ActionPageSetter, self).__init__()
        self.page_number = page_number

    def run(self, context=None):
        if context["locked"]:
            return
        if self.page_number < context["action_page_count"]:
            context["interface_no"] = self.page_number
        super(ActionPageSetter, self).run(context=context)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.page_number)
