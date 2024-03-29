import logging


logger = logging.getLogger()


class BaseAction(object):

    def press(self, context=None):
        pass

    def release(self, context=None):
        pass

    def hold(self, context=None):
        pass

    def run(self, context=None):
        logger.info(self)

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)
