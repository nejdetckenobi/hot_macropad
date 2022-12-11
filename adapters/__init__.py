from importlib import import_module


ADAPTER_DIR = 'adapters'


def get_adapter(adapter_name):
    module_import_string = "{}.{}".format(ADAPTER_DIR, adapter_name.lower())
    module = import_module(module_import_string)
    return getattr(module, adapter_name, None)

