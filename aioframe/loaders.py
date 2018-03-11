import sys
from importlib import import_module
from pkgutil import walk_packages

from .exceptions import AppModuleImportError
from .apps import register


def get_apps_enabled(apps_registry):
    apps_enabled = {}
    for app_name in apps_registry:
        print(app_name)
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
        module_pkg = '{}.{}'.format(app_name, name)
        try:
            sub_module = import_module(module_pkg)
            sub_modules[name] = sub_module
        except ImportError as e:
            raise AppModuleImportError('{}: {}'.format(module_pkg, e))
    return [sub_modules.keys()]


def load_apps_enabled(webapp, conf):
    apps_enabled = get_apps_enabled(conf.APPS_REGISTRY)
    for app_name, app_module in apps_enabled.items():
        try:
            app_views = app_module.views.app_views
        except AttributeError:
            continue
        for view in app_views:
            register(app_module.app_conf.app, webapp, conf)(view)()
        app_module.app_conf.app.load_routes(webapp)


def get_app_models(apps_enabled):
    models = []
    for app in apps_enabled.values():
        try:
            app_models = app.models.app_models
        except AttributeError:
            continue
        models += app_models
    return models
