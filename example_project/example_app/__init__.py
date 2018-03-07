# import sys
# from pkgutil import walk_packages
# from importlib import import_module

# from aioframe.exceptions import AppModuleImportError


# app_module = sys.modules[__name__]
# sub_modules = {}
# for importer, name, is_pkg in walk_packages(app_module.__path__):
#     try:
#         _module = '{}.{}'.format(__name__, name)
#         sub_modules[name] = import_module(_module)
#     except ImportError as e:
#         raise AppModuleImportError('{}: {}'.format(_module, e))

# __all__ = [sub_modules.keys()]

from aioframe.loaders import get_app_modules

__all__ = get_app_modules(__name__)
