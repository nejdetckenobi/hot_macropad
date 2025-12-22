import os
from adapters.base.mixins import ReleaseAction


class PageSetter(ReleaseAction):
    def __init__(self, page_name):
        super(PageSetter, self).__init__()
        self.page_name = page_name

    def run(self, context=None):
        if context["locked"]:
            return

        if self.page_name in context["actions"]:
            context["action_page_name"] = self.page_name
        command = f'python /home/nejdetckenobi/bin/simple_osd.py --text "{self.page_name}" --duration 500 --opacity 0.6 --font-size 36 --x 2600 --y 570'
        os.system(command=command)
        super(PageSetter, self).run(context=context)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.page_name)
