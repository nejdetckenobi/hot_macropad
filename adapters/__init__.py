from importlib import import_module


ADAPTER_DIR = 'adapters'


def get_adapter(adapter_file, adapter_name):
    module_path = "{}.{}".format(ADAPTER_DIR, adapter_file)
    module = import_module(module_path)
    return getattr(module, adapter_name, None)
