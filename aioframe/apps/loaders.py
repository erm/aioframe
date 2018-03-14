import sys
from importlib import import_module
from pkgutil import walk_packages

from ..exceptions import AppModuleImportError


def get_app_modules(app_name):
    app_module = sys.modules[app_name]
    sub_modules = {}
    for importer, name, is_pkg in walk_packages(app_module.__path__):
        module_pkg = '{}.{}'.format(app_name, name)
        try:
            sub_module = import_module(module_pkg)
            sub_modules[name] = sub_module
        except ImportError as e:
            raise AppModuleImportError('{}: {}'.format(module_pkg, e))
    return [sub_modules.keys()]


def get_app_models(apps_enabled):
    models = []
    for app in apps_enabled.values():
        try:
            app_models = app.models.app_models
        except AttributeError:
            continue
        models += app_models
    return models
