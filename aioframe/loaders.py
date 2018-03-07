import sys
from importlib import import_module
from pkgutil import walk_packages

from .exceptions import AppModuleImportError


def get_apps_enabled(apps_registry):
    apps_enabled = {}
    for app_name in apps_registry:
        try:
            app_module = import_module(app_name)
        except ImportError as e:
            raise AppModuleImportError(e)
        apps_enabled[app_name] = app_module
    return apps_enabled


def get_app_modules(app_name):
    app_module = sys.modules[app_name]
    sub_modules = {}
    for importer, name, is_pkg in walk_packages(app_module.__path__):
        try:
            module_pkg = '{}.{}'.format(app_name, name)
            sub_module = import_module(module_pkg)
            sub_modules[name] = sub_module
        except ImportError as e:
            raise AppModuleImportError('{}: {}'.format(_module, e))
    return [sub_modules.keys()]
