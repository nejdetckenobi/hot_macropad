from adapters.base.mixins import ReleaseExecuteActionMixin


class ActionPageSetter(ReleaseExecuteActionMixin):
    def __init__(self, page_name):
        super(ActionPageSetter, self).__init__()
        self.page_name = page_name

    def run(self, context=None):
        if context["locked"]:
            return

        if self.page_name in context["actions"]:
            context["action_page_name"] = self.page_name
            self._write_current_action_page(context=context)

        super(ActionPageSetter, self).run(context=context)

    def _write_current_action_page(self, context):
        if output_file := context.get("action_page_output_file", None):
            with open(output_file, "w") as f:
                f.write(context["action_page_name"])
                f.flush()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.page_name)
