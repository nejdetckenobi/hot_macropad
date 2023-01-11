from adapters.base import ReleaseExecuteAction


class ActionPageSetter(ReleaseExecuteAction):
    def __init__(self, page_name):
        super(ActionPageSetter, self).__init__()
        self.page_name = page_name

    def run(self, context=None):
        if context["locked"]:
            return

        if self.page_name in context["actions"]:
            context["action_page_name"] = self.page_name
        super(ActionPageSetter, self).run(context=context)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.page_name)
