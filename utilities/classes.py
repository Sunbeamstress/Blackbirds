# Python modules.
import importlib

def class_from_name(module_name, class_name):
    m = importlib.import_module(module_name)
    return getattr(m, class_name)